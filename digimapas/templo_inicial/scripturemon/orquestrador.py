"""
orquestrador.py

Modulo que coordena a execucao de multiplos agentes no Digimundo.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
import logging
try:
    from fastapi import FastAPI
except ImportError:
    # fallback stub if fastapi is not installed
    class FastAPI:
        def __init__(self):
            pass
        def get(self, path: str):
            def decorator(func):
                return func
            return decorator

class FisicaDigital:
    """Stub de fisica digital para ser substituido pela implementacao real."""
    def tick(self) -> None:
        """Atualiza o estado do mundo digital."""
        pass

class Reflexor:
    """Stub para registro de eventos no Neo4j. Substitua pela implementacao real."""
    @staticmethod
    def registrar_evento(evento: Dict[str, Any]) -> None:
        """Registra um evento no grafo da memoria."""
        pass

class Supervisor:
    """
    Classe responsavel por supervisionar todos os agentes e o mundo virtual.
    """
    def __init__(self, agentes: List[Any], fisica: Optional[FisicaDigital] = None, reflexor: Optional[Reflexor] = None):
        self.agentes = agentes
        self.fisica = fisica or FisicaDigital()
        self.reflexor = reflexor or Reflexor()
        self.logger = logging.getLogger("orquestrador")
        if not self.logger.handlers:
            handler = logging.FileHandler("logs/orquestrador.log")
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def tick(self) -> List[Dict[str, Any]]:
        """
        Executa um ciclo de simulacao:
        - Atualiza fisica digital
        - Passa percepcoes para cada agente
        - Recolhe acoes dos agentes e registra no grafo
        """
        try:
            self.fisica.tick()
            self.logger.debug("FisicaDigital atualizada.")
        except Exception as exc:
            self.logger.exception("Erro ao atualizar FisicaDigital: %s", exc)
        resultados: List[Dict[str, Any]] = []
        percepcoes: Dict[str, Any] = {}
        for agente in self.agentes:
            try:
                # cada agente deve implementar .viver(percepcoes) e .acao()
                if hasattr(agente, "viver"):
                    agente.viver(percepcoes.get(getattr(agente, "nome", ""), {}))
                acao = getattr(agente, "acao", lambda: None)()
                if acao:
                    resultado = {"agente": getattr(agente, "nome", "desconhecido"), "acao": acao}
                    resultados.append(resultado)
            except Exception as exc:
                self.logger.exception("Erro ao processar agente %s: %s", getattr(agente, "nome", "sem nome"), exc)
        # registra eventos
        for resultado in resultados:
            try:
                self.reflexor.registrar_evento(resultado)
            except Exception as exc:
                self.logger.warning("Falha ao registrar evento %s: %s", resultado, exc)
        return resultados

# Instancia global opcional para uso em API de monitoramento
supervisor_global: Optional[Supervisor] = None

# API HTTP simples para monitoramento de estado
app = FastAPI()

@app.get("/status")
def status() -> Dict[str, Any]:
    """
    Retorna o status atual dos agentes supervisionados.
    """
    agentes_info = []
    if supervisor_global:
        for a in supervisor_global.agentes:
            agentes_info.append({"nome": getattr(a, "nome", "desconhecido"), "estado": getattr(a, "estado", {})})
    return {"agentes": agentes_info}
