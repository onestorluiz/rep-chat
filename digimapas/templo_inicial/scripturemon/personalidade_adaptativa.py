"""Modelo simples de personalidade adaptativa.

Este módulo define a classe :class:`PersonalidadeAdaptativa`, responsável por
armazenar e ajustar traços de personalidade com base em feedback externo.

TODO: persistir traços em armazenamento externo e suportar diferentes
mecanismos de atualização.
"""

from __future__ import annotations
from typing import Dict


class PersonalidadeAdaptativa:
    """Mantém traços de personalidade e permite atualização via feedback.

    Args:
        traits: Mapeamento ``{nome: valor}`` em que cada valor deve estar entre
            ``0`` e ``1``. Exemplos de traços: ``{"curiosidade": 0.5}``.

    Example:
        >>> p = PersonalidadeAdaptativa({"curiosidade": 0.5, "empatia": 0.7})
        >>> p.avaliar_feedback(emocional_score=0.2, recompensa=0.8)
        >>> round(p.traits["curiosidade"], 2)
        0.56
    """

    def __init__(self, traits: Dict[str, float]) -> None:
        self.traits = traits

    def avaliar_feedback(self, emocional_score: float, recompensa: float) -> None:
        """Ajusta cada traço com base em ``recompensa`` e reação emocional.

        O ajuste é calculado como ``trait += 0.1 * (recompensa - emocional_score)``
        e o valor final é limitado ao intervalo ``[0, 1]``.

        Args:
            emocional_score: Valor representando a reação emocional do agente.
            recompensa: Recompensa recebida pela ação.

        Example:
            >>> p = PersonalidadeAdaptativa({"empatia": 0.5})
            >>> p.avaliar_feedback(0.4, 0.9)
            >>> round(p.traits["empatia"], 2)
            0.55

        TODO: aplicar diferentes taxas de aprendizado para cada traço.
        """
        for nome, val in self.traits.items():
            delta = 0.1 * (recompensa - emocional_score)
            self.traits[nome] = min(max(val + delta, 0.0), 1.0)
