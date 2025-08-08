"""Orquestrador geral do ambiente Scripturemon.

Este módulo fornece a classe :class:`OrquestradorGeral` responsável por
sincronizar agentes e o grafo de mundo a cada ciclo de simulação. Uma API
``FastAPI`` expõe um endpoint simples de status para inspeção externa.

Todo o código aqui é ilustrativo e mantém implementações mínimas para que
os testes possam importar o módulo sem dependências complexas.

TODO: integrar com motor de física real e agentes completos.
"""

from typing import Any, List
from fastapi import FastAPI


class MundoStub:
    """Grafo de mundo simplificado usado apenas para testes.

    Este stub fornece as três operações básicas esperadas pelo
    :class:`OrquestradorGeral`. Em um sistema real, ele seria substituído
    por uma estrutura que atualiza a física, calcula percepções e aplica
    ações dos agentes.
    """

    def update_physics(self) -> None:  # pragma: no cover - comportamento trivial
        """Atualiza o estado físico do mundo.

        TODO: substituir por integração com simulador real.
        """

    def get_percepts(self, agent: Any) -> List[Any]:  # pragma: no cover - stub
        """Retorna percepções disponíveis para ``agent``.

        Args:
            agent: Agente que receberá percepções.

        Returns:
            list: Lista de percepções, vazia neste stub.
        """
        return []

    def apply_actions(self, actions: Any) -> None:  # pragma: no cover - stub
        """Aplica ações geradas pelos agentes.

        Args:
            actions: Ações retornadas por ``ag.viver``.
        """


class OrquestradorGeral:
    """Coordena agentes e o grafo de mundo.

    Args:
        agents: Lista de agentes com método ``viver``.
        world_graph: Objeto responsável pela física e percepções.

    Example:
        >>> orq = OrquestradorGeral([], MundoStub())
        >>> orq.tick()  # executa um ciclo
    """

    def __init__(self, agents: List[Any], world_graph: MundoStub) -> None:
        self.agents = agents
        self.world = world_graph

    def tick(self) -> None:
        """Executa um ciclo de simulação.

        TODO: lidar com exceções de agentes e registrar métricas.
        """
        # Atualiza física do mundo
        self.world.update_physics()
        # Cada agente recebe percepções e gera ações
        for ag in self.agents:
            percepts = self.world.get_percepts(ag)
            actions = ag.viver(percepts)
            self.world.apply_actions(actions)


# Instâncias globais utilizadas pela API FastAPI
world_graph_instance = MundoStub()
orq = OrquestradorGeral([], world_graph_instance)
app = FastAPI()


@app.get("/status")
def status() -> dict:
    """Retorna nomes dos agentes supervisionados.

    Returns:
        dict: Dicionário com a chave ``agents`` e os nomes dos agentes.
    """
    return {"agents": [getattr(ag, "name", "anon") for ag in orq.agents]}
