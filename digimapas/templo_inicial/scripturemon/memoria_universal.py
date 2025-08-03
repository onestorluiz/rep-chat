https://github.com/onestorluiz/rep-chat/new/main/digimapas/templo_inicial/scripturemon
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
from typing import List, Optional, Dict

# Importa dependências de memória vetorial e semântica se disponíveis
from .memoria_vetorial import MemoriaVetorial  # type: ignore
try:
    from .memoria_semantica import MemoriaSemantica  # type: ignore
except Exception:
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
    ) -> None:
        """
        Realiza a extração simples de fatos a partir de um evento e um pensamento,
        e atualiza a memória vetorial e semântica conforme necessário.

        Args:
            evento: Texto do evento/pergunta/mensagem recebida.
            pensamento: Texto do pensamento ou resposta gerada pelo agente.
            tags: Lista de rótulos ou categorias associadas à interação (ex.: emoção, prioridade).
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

    def status(self) -> Dict[str, object]:
        """
        Retorna um resumo simples da memória universal.
        """
        return {
            "digimon_id": self.digimon_id,
            "threshold": self.similarity_threshold,
            "total_memorias": self.vetorial.status().get("total_fragmentos", 0),
        }
