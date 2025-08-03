"""
personalidade_adaptativa.py

Modulo que implementa um modelo simples de personalidade adaptativa para um agente.
"""
from __future__ import annotations
from typing import Dict, Optional
import logging
from pathlib import Path
import json

class PersonalidadeAdaptativa:
    """Representa traços de personalidade que se ajustam com o tempo."""
    def __init__(self, nome: str, tracos_iniciais: Optional[Dict[str, float]] = None) -> None:
        self.nome = nome
        # valores padrao para curiosidade, cautela e empatia (0 a 1)
        self.tracos: Dict[str, float] = tracos_iniciais or {
            "curiosidade": 0.5,
            "cautela": 0.5,
            "empatia": 0.5,
        }
        # caminho para registrar historico em markdown
        self.log_path = Path("logs/personalidade.md")
        # configurar logger
        self.logger = logging.getLogger(f"personalidade_{nome}")
        if not self.logger.handlers:
            handler = logging.FileHandler("logs/personalidade.log")
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self._registrar_historico("Inicialização", self.tracos)

    def avaliar_feedback(self, retorno_emocional: float, recompensa: float) -> None:
        """
        Ajusta os traços de personalidade com base em retorno emocional (0-1) e recompensa.
        Feedback positivo aumenta curiosidade e empatia; feedback negativo aumenta cautela.
        """
        try:
            for traco in self.tracos:
                ajuste = 0.0
                if traco == "curiosidade":
                    ajuste = recompensa * 0.1 - (1 - retorno_emocional) * 0.05
                elif traco == "empatia":
                    ajuste = recompensa * 0.08
                elif traco == "cautela":
                    ajuste = (1 - retorno_emocional) * 0.1 - recompensa * 0.05
                # aplica ajuste e limita entre 0 e 1
                self.tracos[traco] = min(max(self.tracos[traco] + ajuste, 0.0), 1.0)
            self._registrar_historico("Ajuste", self.tracos)
        except Exception as e:
            self.logger.exception("Erro ao avaliar feedback: %s", e)

    def ajustar_estilos_de_fala(self) -> Dict[str, str]:
        """
        Gera estilos de fala baseados nos traços de personalidade.
        Maior empatia leva a tom gentil; maior cautela leva a abordagem cautelosa.
        """
        formalidade = "informal" if self.tracos.get("curiosidade", 0) > 0.7 else "formal"
        tom = "gentil" if self.tracos.get("empatia", 0) > 0.6 else "neutro"
        cautela = "cauteloso" if self.tracos.get("cautela", 0) > 0.6 else "direto"
        estilo = {"formalidade": formalidade, "tom": tom, "cautela": cautela}
        self._registrar_historico("Ajuste estilo", estilo)
        return estilo

    def _registrar_historico(self, evento: str, dados: Dict[str, float] | Dict[str, str]) -> None:
        """
        Registra um evento de mudança da personalidade no arquivo markdown e no logger.
        """
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(f"### {evento}\n\n")
                f.write(json.dumps(dados, ensure_ascii=False, indent=2))
                f.write("\n\n")
            self.logger.info("Evento '%s' registrado: %s", evento, dados)
        except Exception as e:
            self.logger.exception("Erro ao registrar histórico: %s", e)
