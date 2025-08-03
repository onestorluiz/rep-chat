"""
Modulo de Memoria Semantica Agentica (A-MEM) para Scripturemon.

Este modulo implementa uma memoria de longo prazo baseada em notas atomicas interconectadas,
inspirada em sistemas Zettelkasten e frameworks de agentic memory. A ideia e permitir que o
Scripturemon construa uma teia de significados, conectando experiencias semelhantes por tema,
causa ou emocao.
"""

import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class NotaSemantica:
    """Representa uma nota atomica na memoria semantica."""
    conteudo: str
    tags: List[str] = field(default_factory=list)
    relacionamentos: Dict[str, List[str]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

class MemoriaSemantica:
    """
    Memoria semantica para o Scripturemon.

    Esta classe armazena notas semanticas interconectadas. Cada nota pode estar ligada a outras notas
    por relacoes explicitas. Para manter as coisas simples, notas sao persistidas em arquivos JSON
    dentro de um diretorio de armazenamento.
    """

    def __init__(self, persist_dir: str = "digimapas/templo_inicial/scripturemon/memoria_semantica_store"):
        # Diretorio onde as notas serao persistidas
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        # Mapeamento de ID de nota para instancia NotaSemantica
        self.notas: Dict[str, NotaSemantica] = {}

    def registrar_nota(self, conteudo: str, tags: List[str] = None, links: Dict[str, List[str]] = None) -> str:
        """
        Cria uma nova nota semantica e salva no armazenamento.

        :param conteudo: Texto da experiencia ou pensamento.
        :param tags: Lista opcional de tags associadas (conceitos, temas ou entidades).
        :param links: Dicionario opcional de relacionamentos para outras notas, indexado por tipo de relacao.
        :return: Identificador unico da nota criada.
        """
        nota_id = datetime.utcnow().isoformat()
        nota = NotaSemantica(conteudo=conteudo, tags=tags or [], relacionamentos=links or {})
        self.notas[nota_id] = nota
        self._salvar_nota(nota_id, nota)
        return nota_id

    def _salvar_nota(self, nota_id: str, nota: NotaSemantica) -> None:
        """Salva a nota em disco como JSON."""
        path = os.path.join(self.persist_dir, f"{nota_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "conteudo": nota.conteudo,
                "tags": nota.tags,
                "relacionamentos": nota.relacionamentos,
                "created_at": nota.created_at.isoformat()
            }, f, ensure_ascii=False, indent=2)

    def carregar_notas(self) -> None:
        """Carrega todas as notas persistidas do diretorio para a memoria em execucao."""
        for filename in os.listdir(self.persist_dir):
            if filename.endswith(".json"):
                nota_id = filename[:-5]
                with open(os.path.join(self.persist_dir, filename), encoding="utf-8") as f:
                    data = json.load(f)
                nota = NotaSemantica(
                    conteudo=data.get("conteudo", ""),
                    tags=data.get("tags", []),
                    relacionamentos=data.get("relacionamentos", {}),
                    created_at=datetime.fromisoformat(data["created_at"])
                )
                self.notas[nota_id] = nota

    def buscar_por_tag(self, tag: str) -> List[NotaSemantica]:
        """Retorna uma lista de notas que contem a tag especificada."""
        return [nota for nota in self.notas.values() if tag in nota.tags]

    def adicionar_relacionamento(self, origem_id: str, destino_id: str, tipo: str) -> None:
        """
        Adiciona um relacionamento entre duas notas existentes.

        :param origem_id: ID da nota de origem.
        :param destino_id: ID da nota de destino.
        :param tipo: Tipo da relacao (ex.: "mesmo_tema", "consequencia", etc.).
        """
        origem = self.notas.get(origem_id)
        if not origem:
            raise KeyError(f"Nota de origem {origem_id} nao encontrada.")
        origem.relacionamentos.setdefault(tipo, []).append(destino_id)
        # Atualiza persistencia
        self._salvar_nota(origem_id, origem)
