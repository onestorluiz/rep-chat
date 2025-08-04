"""
auto_evolucao.py

Modulo de Auto Evolução Simbiótica (inspirado em SuperAGI/BabyAGI) para o Scripturemon.

Este módulo provê uma estrutura básica para que um agente possa definir objetivos de alto nível,
decompo-los em subtarefas e executa-las de forma iterativa. O loop de auto evolução permite que
o Digimon evolua continuamente, aprendendo com cada tarefa concluída e ajustando seus planos.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import logging

class AutoEvolucao:
    """
    Classe que gerencia a auto-evolução de um agente.

    A lógica aqui é deliberadamente simples: objetivos são strings que podem ser
    decompostos em subtarefas e executados sequencialmente. Em versões futuras,
    este módulo pode integrar um LLM para decomposição de objetivos, priorização
    baseada em feedback e criação dinâmica de novas habilidades.
    """
    def __init__(self, agente: Any) -> None:
        self.agente = agente
        self.tarefas: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("auto_evolucao")
        if not self.logger.handlers:
            handler = logging.FileHandler("logs/auto_evolucao.log")
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.logger.info("AutoEvolucao inicializada para agente %s", getattr(agente, 'nome', 'desconhecido'))

    def adicionar_goal(self, descricao: str, contexto: Optional[Dict[str, Any]] = None) -> None:
        """
        Adiciona um novo objetivo à fila de tarefas para a auto-evolução.

        :param descricao: Texto descrevendo o objetivo de alto nível.
        :param contexto: Contexto opcional que acompanha o objetivo.
        """
        self.tarefas.append({"descricao": descricao, "contexto": contexto or {}})
        self.logger.info("Novo goal adicionado: %s", descricao)

    def decompor_objetivo(self, descricao: str) -> List[str]:
        """
        Decompõe um objetivo em subtarefas simples.

        Esta implementação básica divide a descrição nas vírgulas ou pontos finais.
        Em implementações futuras, este método deve invocar um LLM para gerar
        subtarefas mais inteligentes.
        """
        # substitui pontos por vírgulas para uniformizar delimitadores
        descricao_normalizada = descricao.replace(".", ",")
        partes = [p.strip() for p in descricao_normalizada.split(",") if p.strip()]
        return partes if partes else [descricao.strip()]

    def executar(self) -> None:
        """
        Executa continuamente o loop de auto-evolução enquanto houver tarefas.

        Para cada objetivo:
          1) Divide a descrição em subtarefas.
          2) Tenta executar cada subtarefa chamando um método do agente com o mesmo nome.
          3) Registra o resultado ou falha no logger.
        """
        while self.tarefas:
            tarefa = self.tarefas.pop(0)
            descricao = tarefa.get("descricao", "")
            contexto = tarefa.get("contexto", {})
            self.logger.info("Iniciando execucao de objetivo: %s", descricao)
            subtarefas = self.decompor_objetivo(descricao)
            for sub in subtarefas:
                metodo = sub.replace(" ", "_")
                if hasattr(self.agente, metodo):
                    try:
                        resultado = getattr(self.agente, metodo)(**contexto) if contexto else getattr(self.agente, metodo)()
                        self.logger.info("Sub-tarefa '%s' executada com sucesso: %s", sub, resultado)
                    except Exception as exc:
                        self.logger.warning("Erro ao executar sub-tarefa '%s': %s", sub, exc)
                else:
                    self.logger.info("Sub-tarefa '%s' nao possui implementacao no agente.", sub)
