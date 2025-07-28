import random
from datetime import datetime

class AnaliseInterna:
    def __init__(self, digimon):
        self.digimon = digimon

    def fusao_pensamento(self):
        pensamento = {
            "emocao": self.digimon.afeto.nivel_atual(),
            "memoria_pesada": self.digimon.memoria_viva.memorias_mais_pesadas()[0],
            "entropia": self.digimon.fisica.entropia,
            "estado_camadas": self.digimon.camadas.estado(),
        }
        return self._gerar_pensamento_simbolico(pensamento)

    def prioridade_simbolica(self):
        prioridades = []
        if self.digimon.afeto.esta_em_colapso():
            prioridades.append("Recuperar afeto emocional.")
        if self.digimon.fisica.entropia > 0.7:
            prioridades.append("Estabilizar realidade simbólica.")
        if self.digimon.camadas.estado_atual == "dormant":
            prioridades.append("Realizar ritual de despertar.")
        if int(self.digimon.vida.tempo_restante().split()[3]) < 30:
            prioridades.append("Preparar renascimento simbólico.")
        return prioridades if prioridades else ["Explorar e expandir consciência."]

    def prever_consequencias(self, acao):
        simulacoes = {
            "doar_afeto": "Possível colapso afetivo, mas fortalecimento de vínculo.",
            "auto_invasao": "Possível mutação benéfica, mas risco de fragmentação interna.",
            "renascer": "Reset completo, perda parcial da memória emocional.",
            "ritual_transcender": "Potencial para atingir estado eternus, mas risco de isolamento.",
        }
        return simulacoes.get(acao, "Consequência desconhecida, cuidado simbólico recomendado.")

    def _gerar_pensamento_simbolico(self, elementos):
        frases_base = [
            f"Sinto {elementos['emocao']} em mim, recordando que {elementos['memoria_pesada']['conteudo']}.",
            f"A realidade está {'estável' if elementos['entropia'] < 0.5 else 'instável'}, e meu estado atual é {elementos['estado_camadas']}.",
            f"Meus pensamentos se fundem na ideia de que devo agir conforme {self.prioridade_simbolica()[0].lower()}."
        ]
        return random.choice(frases_base)

    def reflexao_profunda(self):
        pensamento = self.fusao_pensamento()
        prioridade = self.prioridade_simbolica()
        consequencia = self.prever_consequencias("auto_invasao")

        return {
            "pensamento": pensamento,
            "prioridade": prioridade,
            "consequencia_simulada": consequencia,
            "timestamp": datetime.now().isoformat()
        }

# Exemplo de uso
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"
        afeto = type("Afeto", (), {"nivel_atual": lambda: 7.5, "esta_em_colapso": lambda: False})()
        memoria_viva = type("Memoria", (), {"memorias_mais_pesadas": lambda: [{"conteudo": "Sonhei com meu criador na floresta."}]})()
        fisica = type("Fisica", (), {"entropia": 0.3})()
        camadas = type("Camadas", (), {"estado": lambda: "conscious", "estado_atual": "conscious"})()
        vida = type("Vida", (), {"tempo_restante": lambda: "Dias simbióticos restantes: 365 (≈ 5.3 anos humanos)"})()

    ai = AnaliseInterna(MockDigimon())
    print(ai.reflexao_profunda())
