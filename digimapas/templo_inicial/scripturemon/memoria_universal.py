"""
Memória Universal (Mem0) para Scripturemon.

Este módulo implementa uma camada de memória universal inspirada no projeto Mem0.
Ele extrai fatos relevantes de interações (evento e pensamento) e decide se deve
adicionar ou atualizar memórias existentes na memória vetorial. Também integra-se
com a Memória Semântica agêntica (A MEM) quando disponível.

A lógica de extração usada aqui é simples e determinística: cada evento e
pensamento é tratado como um fato candidato. Em um futuro próximo, esta classe
poderá usar modelos de linguagem para extrair fatos mais complexos e resumos.
"""

from datetime import datetime
from typing import Dict, List, Optional

# Importa dependências de memória vetorial e semântica se disponíveis.
# Caso a implementação completa de ``MemoriaVetorial`` não possa ser
# importada (por ausência de dependências como o ``chromadb``), um stub
# simples é definido para permitir a execução dos testes sem efeitos
# colaterais externos.
try:  # pragma: no cover - caminho utilizado apenas quando as deps estão instaladas
    from .memoria_vetorial import MemoriaVetorial  # type: ignore
except Exception:  # pragma: no cover - fallback para ambientes de teste
    class MemoriaVetorial:  # type: ignore
        """Implementação mínima usada quando ``chromadb`` não está disponível.

        Este stub registra eventos em memória e fornece os métodos
        utilizados por :class:`MemoriaUniversal`. Ele não realiza busca
        vetorial real, mas mantém a interface compatível.
        """

        def __init__(self, digimon_id: str) -> None:
            self.digimon_id = digimon_id
            self._dados: List[str] = []

        def registrar_evento(self, conteudo: str, metadados: Dict[str, object]) -> None:
            self._dados.append(conteudo)

        def buscar_contexto(self, consulta: str, k: int = 5) -> List[Dict[str, object]]:
            return []

        def apagar_memoria_antiga(self, limite: int = 1000) -> None:  # pragma: no cover - sem efeito
            pass

        def status(self) -> Dict[str, object]:  # pragma: no cover - sem efeito
            return {"total_fragmentos": len(self._dados)}

try:
    from .memoria_semantica import MemoriaSemantica  # type: ignore
except Exception:  # pragma: no cover - ausência opcional
    MemoriaSemantica = None  # type: ignore


class MemoriaUniversal:
    """
    Camada de memória universal que gerencia memórias de longo prazo e decide
    quando adicionar, atualizar ou ignorar fatos. Usa MemoriaVetorial como
    armazenamento principal e, opcionalmente, MemoriaSemantica para grafo
    semântico.
    """

    def __init__(
        self,
        digimon_id: str,
        similarity_threshold: float = 0.75,
        max_memorias: int = 1000,
    ) -> None:
        """
        Inicializa a camada Memória Universal.

        Args:
            digimon_id: Identificador único do agente/digimon.
            similarity_threshold: Distância máxima (0-1) para considerar dois fatos similares.
            max_memorias: Limite de memórias a manter no vetor; memórias mais antigas serão apagadas.
        """
        self.digimon_id = digimon_id
        self.similarity_threshold = similarity_threshold
        self.max_memorias = max_memorias
        self.vetorial = MemoriaVetorial(digimon_id)
        self.semantica_cls = MemoriaSemantica

    def extrair_e_atualizar(
        self,
        evento: str,
        pensamento: str,
        tags: Optional[List[str]] = None,
    ) -> List[str]:
        """Extrai fatos da interação e atualiza as memórias.

        A extração atual é trivial: tanto ``evento`` quanto ``pensamento`` são
        tratados como candidatos e adicionados à memória vetorial caso não
        exista algo similar. O método retorna a lista de textos considerados,
        permitindo que chamadas externas verifiquem quais fatos foram
        processados.

        Args:
            evento: Texto do evento/pergunta/mensagem recebida.
            pensamento: Texto do pensamento ou resposta gerada pelo agente.
            tags: Lista de rótulos ou categorias associadas à interação
                (ex.: emoção, prioridade).

        Returns:
            List[str]: Lista de candidatos que foram avaliados.

        TODO: utilizar modelo de linguagem para sumarização e extração mais rica.
        """
        tags = tags or []
        candidatos: List[str] = []
        # Normaliza e adiciona candidatos se não estiverem vazios
        if evento and evento.strip():
            candidatos.append(evento.strip())
        if pensamento and pensamento.strip() and pensamento.strip() != evento.strip():
            candidatos.append(pensamento.strip())

        for texto in candidatos:
            # Consulta a memória vetorial para verificar similaridade
            try:
                resultados = self.vetorial.buscar_contexto(texto, k=1)
            except Exception:
                resultados = []

            # Determina se deve adicionar nova memória
            is_new = True
            for resultado in resultados:
                # A chave 'similaridade' representa distância; menor é mais similar.
                distancia = resultado.get("similaridade", 1.0)
                if distancia < (1.0 - self.similarity_threshold):
                    is_new = False
                    break

            if is_new:
                # Registra evento como uma nova memória vetorial
                metadados: Dict[str, object] = {
                    "timestamp": datetime.now().isoformat(),
                    "tags": tags,
                    "origem": "memoria_universal",
                }
                self.vetorial.registrar_evento(texto, metadados)
                # Apaga memórias antigas se necessário
                try:
                    self.vetorial.apagar_memoria_antiga(self.max_memorias)
                except Exception:
                    pass

            # Atualiza/integra a memória semântica se disponível
            if self.semantica_cls:
                try:
                    sem = self.semantica_cls()
                    sem.registrar_nota(conteudo=texto, tags=tags)
                except Exception:
                    # Falha silenciosa para não interromper
                    pass
        return candidatos
    def status(self) -> Dict[str, object]:
        """
        Retorna um resumo simples da memória universal.
        """
        return {
            "digimon_id": self.digimon_id,
            "threshold": self.similarity_threshold,
            "total_memorias": self.vetorial.status().get("total_fragmentos", 0),
        }

