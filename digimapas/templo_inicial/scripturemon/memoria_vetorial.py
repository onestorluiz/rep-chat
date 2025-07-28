import os
from typing import List, Dict, Any
from datetime import datetime
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

class MemoriaVetorial:
    def __init__(self, digimon_id: str, persist_dir: str = "./memoria_vetorial/db"):
        self.digimon_id = digimon_id
        self.client = chromadb.Client(Settings(persist_directory=persist_dir))
        self.embedding_fn = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection = self.client.get_or_create_collection(name=digimon_id, embedding_function=self.embedding_fn)

    def registrar_evento(self, conteudo: str, metadados: Dict[str, Any]) -> None:
        uid = f"{self.digimon_id}-{datetime.now().isoformat()}"
        self.collection.add(documents=[conteudo], metadatas=[metadados], ids=[uid])

    def buscar_contexto(self, consulta: str, k: int = 5) -> List[Dict[str, Any]]:
        resultados = self.collection.query(query_texts=[consulta], n_results=k)
        return [
            {
                "documento": doc,
                "metadados": meta,
                "similaridade": score
            }
            for doc, meta, score in zip(resultados["documents"][0], resultados["metadatas"][0], resultados["distances"][0])
        ]

    def apagar_memoria_antiga(self, limite: int = 1000) -> None:
        all_ids = self.collection.get()["ids"]
        if len(all_ids) > limite:
            excesso = all_ids[:len(all_ids) - limite]
            self.collection.delete(excesso)

    def status(self) -> Dict[str, Any]:
        return {
            "total_fragmentos": len(self.collection.get()["ids"]),
            "nome": self.digimon_id
        }
