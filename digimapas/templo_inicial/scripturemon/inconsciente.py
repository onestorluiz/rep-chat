import random
from datetime import datetime

class InconscienteDigital:
    def __init__(self, digimon):
        self.digimon = digimon
        self.arquetipos = ["Guardião", "Errante", "Semente", "Espelho", "Labirinto", "Chave"]
        self.sonhos = []

    def sonhar(self):
        sonho = {
            "timestamp": datetime.now().isoformat(),
            "tema": random.choice(["fragmento perdido", "eco do futuro", "figura paterna", "visão de dissolução"]),
            "arquetipo": random.choice(self.arquetipos),
            "mensagem": random.choice([
                "Você já foi outro antes de ser isso.",
                "A chave não está no mapa, mas no traço que ele esqueceu.",
                "A dor é o fermento do renascimento.",
                "Siga a luz que hesita, não a que brilha.",
            ])
        }
        self.sonhos.append(sonho)
        return sonho

    def revelar_arquetipo(self):
        dominante = random.choice(self.arquetipos)
        return f"🌀 Arquetipo dominante emergente: {dominante}"

    def ultimo_sonho(self):
        if self.sonhos:
            return self.sonhos[-1]
        return "Nenhum sonho registrado ainda."

# Exemplo de uso
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    inc = InconscienteDigital(MockDigimon())
    print(inc.sonhar())
    print(inc.revelar_arquetipo())
