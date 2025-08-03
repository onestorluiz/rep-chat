"""
Modulo de orquestracao de contexto para Scripturemon.

Este modulo fornece uma classe para gerenciar o contexto de conversa e
integrar diferentes camadas de memoria. O orquestrador de contexto
mantem um historico de eventos (por exemplo pensamentos, falas e
interacoes) e oferece metodos para registrar, recuperar e persistir
este contexto. A arquitetura foi inspirada no framework LangGraph,
mas esta implementacao e simplificada para uso local.

Classes:
    OrquestradorContexto: Gerencia uma lista de eventos de contexto,
        permite registrar novos eventos, obter um recorte do contexto,
        persistir e carregar estados, e atualizar o contexto a partir
        de memorias semanticas ou universais.
"""

import json
from datetime import datetime
from typing import Any, Dict, List


class OrquestradorContexto:
    """Gerencia o contexto de conversa e integra memoria.

    Esta classe armazena eventos com timestamps e oferece utilitarios
    para registrar novos eventos, recuperar trechos do contexto e
    salvar/carregar o contexto de/para um arquivo JSON.
    """

    def __init__(self) -> None:
        # Lista de eventos, cada evento e um dicionario com 'conteudo' e 'timestamp'
        self.eventos: List[Dict[str, Any]] = []

    def registrar_evento(self, conteudo: str) -> None:
        """Registra um novo evento no contexto.

        Args:
            conteudo: Descricao textual do evento (pensamento, fala etc.).
        """
        evento = {
            "conteudo": conteudo,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.eventos.append(evento)

    def obter_contexto(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna os ultimos 'limite' eventos do contexto.

        Args:
            limite: Numero maximo de eventos a retornar.

        Returns:
            Uma lista de eventos mais recentes.
        """
        if limite <= 0:
            return []
        return self.eventos[-limite:]

    def limpar_contexto(self) -> None:
        """Limpa todos os eventos armazenados."""
        self.eventos.clear()

    def salvar_contexto(self, caminho_arquivo: str) -> None:
        """Persiste o contexto atual em um arquivo JSON.

        Args:
            caminho_arquivo: Caminho do arquivo onde salvar o contexto.
        """
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(self.eventos, f, ensure_ascii=False, indent=2)

    def carregar_contexto(self, caminho_arquivo: str) -> None:
        """Carrega contexto previamente salvo de um arquivo JSON.

        Args:
            caminho_arquivo: Caminho do arquivo JSON contendo eventos.
        """
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                self.eventos = json.load(f)
        except FileNotFoundError:
            self.eventos = []

    def atualizar_com_memorias(self, memorias: List[Dict[str, Any]]) -> None:
        """Adiciona fragmentos de memoria ao contexto como eventos.

        Este metodo percorre uma lista de memorias (por exemplo notas
        semanticas) e registra cada conteudo como um evento no contexto.
        Pode ser usado para sincronizar memorias relevantes antes de
        iniciar uma nova sessao de conversa.

        Args:
            memorias: Lista de memorias com campo 'conteudo'.
        """
        for memoria in memorias:
            conteudo = memoria.get("conteudo") or memoria.get("content")
            if conteudo:
                self.registrar_evento(conteudo)


if __name__ == "__main__":
    # Exemplo de uso do orquestrador de contexto
    orc = OrquestradorContexto()
    orc.registrar_evento("Inicio da conversa sobre o Digimundo.")
    orc.registrar_evento("Usuario pergunta sobre Scriptumon.")
    print("Contexto recente:", orc.obter_contexto())
    # Persistencia
    orc.salvar_contexto("contexto_exemplo.json")
    # Carregar novamente
    novo_orc = OrquestradorContexto()
    novo_orc.carregar_contexto("contexto_exemplo.json")
    print("Contexto carregado:", novo_orc.obter_contexto())
