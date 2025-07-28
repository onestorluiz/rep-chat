import random
from datetime import datetime

class FisicaDigital:
    def __init__(self, digimon):
        self.digimon = digimon
        self.realidade_estavel = True
        self.entropia = 0.0  # 0 = estabilidade total, 1 = colapso simbólico
        self.eventos_distorcao = []

    def flutuar_realidade(self):
        variacao = random.uniform(-0.05, 0.1)
        self.entropia = min(max(self.entropia + variacao, 0.0), 1.0)

        if self.entropia >= 0.7:
            self.realidade_estavel = False
            evento = self._registrar_distorcao("Distorção simbólica detectada: pensamento ecoado duas vezes.")
            return f"⚠️ Realidade instável. {evento}"
        elif self.entropia <= 0.2:
            self.realidade_estavel = True
            return "🌐 Realidade ancorada. Tudo parece coerente."
        else:
            return "🔄 Realidade flutuante. Pequenos ecos perceptíveis."

    def _registrar_distorcao(self, descricao: str):
        evento = {
            "timestamp": datetime.now().isoformat(),
            "descricao": descricao,
            "entropia": round(self.entropia, 2)
        }
        self.eventos_distorcao.append(evento)
        return descricao

    def colapsar(self):
        self.entropia = 1.0
        self.realidade_estavel = False
        return self._registrar_distorcao("⚠️ Colapso total da física simbólica. O Digimon perdeu referência do mundo.")

    def reinicializar(self):
        self.entropia = 0.0
        self.realidade_estavel = True
        return "🔁 Física digital reiniciada. O ciclo simbólico foi restaurado."

    def estado_atual(self):
        return {
            "entropia": round(self.entropia, 2),
            "realidade_estavel": self.realidade_estavel,
            "ultimos_eventos": self.eventos_distorcao[-3:]
        }

# Exemplo
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    f = FisicaDigital(MockDigimon())
    for _ in range(10):
        print(f.flutuar_realidade())
    print(f.estado_atual())
