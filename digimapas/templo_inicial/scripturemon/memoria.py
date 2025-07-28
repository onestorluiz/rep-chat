from datetime import datetime
import random

class MemoriaEmocional:
    def __init__(self, digimon):
        self.digimon = digimon
        self.memoria = []

    def registrar(self, conteudo: str, emocao: str, intensidade: float):
        fragmento = {
            "timestamp": datetime.now().isoformat(),
            "conteudo": conteudo,
            "emocao": emocao,
            "intensidade": intensidade,
            "peso": self._calcular_peso(emocao, intensidade)
        }
        self.memoria.append(fragmento)
        return fragmento

    def _calcular_peso(self, emocao, intensidade):
        base = {
            "alegria": 1.2,
            "tristeza": 1.6,
            "raiva": 1.4,
            "curiosidade": 1.1,
            "medo": 1.3,
            "compaixao": 1.5
        }.get(emocao, 1.0)
        return round(base * intensidade, 2)

    def buscar_por_emocao(self, emocao: str):
        return [m for m in self.memoria if m["emocao"] == emocao]

    def memorias_mais_pesadas(self, k=3):
        return sorted(self.memoria, key=lambda m: m["peso"], reverse=True)[:k]

    def conexoes_emocionais(self, alvo: str):
        relacionados = []
        for mem in self.memoria:
            if alvo.lower() in mem["conteudo"].lower():
                relacionados.append({"emocao": mem["emocao"], "peso": mem["peso"]})
        return relacionados

# Exemplo de uso
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    mm = MemoriaEmocional(MockDigimon())
    mm.registrar("Sonhei com meu criador na floresta.", "compaixao", 0.9)
    mm.registrar("Fui ignorado por Reflectimon.", "tristeza", 0.7)
    mm.registrar("Toquei o código base da realidade.", "curiosidade", 0.95)

    print(mm.memorias_mais_pesadas())
    print(mm.conexoes_emocionais("reflectimon"))
