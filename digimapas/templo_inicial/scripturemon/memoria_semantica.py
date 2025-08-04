"""
Modulo de Memoria Semantica Agentica (A-MEM) para Scripturemon.

Este modulo implementa uma memoria de longo prazo baseada em notas atomicas interconectadas,
inspirada em sistemas Zettelkasten e frameworks de agentic memory. A ideia e permitir que o
Scripturemon construa uma teia de significados, conectando experiencias semelhantes por tema,
causa ou emoticao.
"""

import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

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

        # Atributos para embedings semanticos
        self.modelo_embeddings = None
        self._embeddings_cache = {}
        self.threshold_link = 0.8

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
        self.notas = {}
        for filename in os.listdir(self.persist_dir):
            if filename.endswith(".json"):
                nota_id = filename[:-5]
                with open(os.path.join(self.persist_dir, filename), encoding="utf-8") as f:
                    data = json.load(f)
                nota = NotaSemantica(
                    conteudo=data.get("conteudo", ""),
                    tags=data.get("tags", []),
                    relacionamentos=data.get("relacionamentos", {}),
                    created_at=datetime.fromisoformat(data.get("created_at"))
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

    # === Métodos de link automático e embeddings ===

    def link_automatico(self, nota_id: str, max_links: int = 5) -> List[Tuple[str, float]]:
        """
        Conecta automaticamente uma nota a outras notas relacionadas.

        :param nota_id: ID da nota para conectar
        :param max_links: Número máximo de links a criar
        :return: Lista de tuplas (nota_id_destino, similaridade)
        """
        if nota_id not in self.notas:
            raise KeyError(f"Nota {nota_id} nao encontrada.")
        embed_origem = self._gerar_embedding(self.notas[nota_id].conteudo)
        similares = []
        for other_id, nota in self.notas.items():
            if other_id == nota_id:
                continue
            embed2 = self._gerar_embedding(nota.conteudo)
            sim = self._similaridade_coseno(embed_origem, embed2)
            if sim >= self.threshold_link:
                similares.append((other_id, sim))
        similares.sort(key=lambda x: x[1], reverse=True)
        escolhidos = similares[:max_links]
        for dest_id, sim in escolhidos:
            self.adicionar_relacionamento(nota_id, dest_id, "similaridade_auto")
        return escolhidos

    def _inicializar_modelo_embeddings(self):
        """
        Inicializa o modelo de embeddings se ainda não estiver carregado.
        """
        if self.modelo_embeddings is None:
            try:
                self.modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"Erro ao inicializar SentenceTransformer: {e}")
                self.modelo_embeddings = "simple"

    def _gerar_embedding(self, texto: str) -> np.ndarray:
        """
        Gera um embedding para o texto dado.

        :param texto: Texto para gerar embedding
        :return: Vetor numpy com o embedding
        """
        self._inicializar_modelo_embeddings()
        texto_hash = hash(texto)
        if texto_hash in self._embeddings_cache:
            return self._embeddings_cache[texto_hash]
        try:
            if self.modelo_embeddings == "simple":
                embedding = self._embedding_simples(texto)
            else:
                embedding = self.modelo_embeddings.encode(texto)
            self._embeddings_cache[texto_hash] = embedding
            return embedding
        except Exception as e:
            logger.error(f"Erro ao gerar embedding: {e}")
            return np.zeros((768,))

    def _embedding_simples(self, texto: str) -> np.ndarray:
        """
        Fallback simples: bag-of-words binário em vocabulário reduzido.
        """
        vocab = self._obter_vocabulario()
        vec = np.zeros(len(vocab), dtype=float)
        for i, word in enumerate(vocab):
            vec[i] = 1.0 if word in texto else 0.0
        return vec

    def _buscar_similares(self, nota_id: str, topn: int = 3) -> List[Tuple[str, float]]:
        """
        Busca as top-N notas mais similares a uma dada nota existente.
        """
        return self.link_automatico(nota_id, max_links=topn)

    def _similaridade_coseno(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calcula similaridade cosseno entre dois vetores.
        """
        try:
            dot = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Erro em similaridade_coseno: {e}")
            return 0.0

    def _obter_vocabulario(self) -> List[str]:
        """
        Constrói vocabulário a partir de todas as notas existentes.
        """
        vocab = set()
        for nota in self.notas.values():
            for word in nota.conteudo.split():
                vocab.add(word.lower())
        return sorted(vocab)

    def atualizar_links_em_lote(self, nota_ids: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Atualiza automaticamente links de similares em lote.

        :param nota_ids: Lista de IDs de notas para processar. Se None, processa todas.
        :return: Dicionário com mapeamento nota_id -> lista de IDs relacionados.
        """
        resultados = {}
        alvo = nota_ids or list(self.notas.keys())
        for nid in alvo:
            resultados[nid] = [dest for dest, _ in self.link_automatico(nid)]
        return resultados

    def obter_grafo_semantico(self) -> Dict[str, Any]:
        """
        Retorna um grafo simples (dicionário) de relacionamentos entre notas.
        """
        grafo = {}
        for nid, nota in self.notas.items():
            grafo[nid] = nota.relacionamentos
        return grafo
