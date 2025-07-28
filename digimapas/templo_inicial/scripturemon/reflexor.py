from typing import List, Dict, Any
from datetime import datetime
from neo4j import GraphDatabase

class Reflexor:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def registrar_triplas(self, nome_digimon: str, memorias: List[Dict[str, Any]]):
        with self.driver.session() as session:
            for memoria in memorias:
                sujeito = nome_digimon
                relacao = memoria.get("type", "viveu")
                objeto = memoria.get("content", "experiencia")
                timestamp = memoria.get("timestamp", datetime.now()).isoformat()
                sig = memoria.get("significance", 0.5)

                session.run(
                    """
                    MERGE (s:Digimon {nome: $sujeito})
                    MERGE (o:Experiencia {descricao: $objeto})
                    MERGE (s)-[r:%s {timestamp: $timestamp, significado: $sig}]->(o)
                    """ % relacao.upper(),
                    sujeito=sujeito,
                    objeto=objeto,
                    timestamp=timestamp,
                    sig=sig
                )

    def consultar_relacoes(self, nome_digimon: str) -> List[str]:
        with self.driver.session() as session:
            resultado = session.run(
                """
                MATCH (s:Digimon {nome: $nome})-[r]->(o:Experiencia)
                RETURN type(r) AS relacao, o.descricao AS experiencia, r.timestamp AS quando
                ORDER BY r.timestamp DESC
                LIMIT 10
                """,
                nome=nome_digimon
            )
            return [f"{record['relacao']} -> {record['experiencia']} ({record['quando']})" for record in resultado]

    def status(self) -> Dict[str, Any]:
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as total")
                count = result.single()["total"]
                return {"conectado": True, "total_nos": count}
        except Exception as e:
            return {"conectado": False, "erro": str(e)}
