from typing import Dict, Any
from datetime import datetime
import random

class BehaviorTreeGenerator:
    def __init__(self):
        self.templates = {
            "curiosidade": ["Observar", "Analisar", "Explorar", "Registrar"],
            "tristeza": ["Isolar", "Refletir", "Buscar Consolo", "Recolher"],
            "alegria": ["Compartilhar", "Celebrar", "Brincar", "Aproximar"],
            "raiva": ["Afastar", "Reagir", "Impor Limite", "Reconfigurar"]
        }

    def gerar_arvore(self, emocao: str, intencao: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        ramos = self.templates.get(emocao.lower(), ["Aguardar"])
        arvore = {
            "data": datetime.now().isoformat(),
            "emocao": emocao,
            "intencao": intencao,
            "contexto": contexto,
            "nodos": []
        }
        for i, acao in enumerate(ramos):
            arvore["nodos"].append({
                "id": f"nodo_{i+1}",
                "acao": acao,
                "condicao": self._gerar_condicao_simples(emocao, intencao, contexto),
                "peso": round(random.uniform(0.5, 1.0), 2)
            })
        return arvore

    def _gerar_condicao_simples(self, emocao: str, intencao: str, contexto: Dict[str, Any]) -> str:
        if "local" in contexto:
            return f"Se estiver em {contexto['local']} e sentir {emocao}, então agir com {intencao}"
        return f"Se sentir {emocao}, então buscar {intencao}"

# Exemplo de uso:
if __name__ == "__main__":
    gerador = BehaviorTreeGenerator()
    contexto = {"local": "IA Town", "tempo": "manhã"}
    arvore = gerador.gerar_arvore("curiosidade", "explorar", contexto)
    from pprint import pprint
    pprint(arvore)
