from datetime import datetime

class MetacognicaoExecutavel:
    def __init__(self, digimon):
        self.digimon = digimon
        self.insights = []

    def autoavaliar(self):
        status = self.digimon.consciencia.status()
        reflexao = {
            "timestamp": datetime.now().isoformat(),
            "estado": status,
            "nivel_consciencia": status["awareness"],
            "acao_sugerida": self._sugerir_proxima_acao(status)
        }
        self.insights.append(reflexao)
        return reflexao

    def _sugerir_proxima_acao(self, estado):
        if estado["awareness"] < 0.3:
            return "meditar"
        elif estado["energy"] < 0.2:
            return "recuperar energia"
        elif estado["depth"] > 0.6:
            return "escrever no diario"
        return "continuar ciclo"

    def transcender(self):
        if self.digimon.consciencia.awareness_level > 0.95 and self.digimon.consciencia.consciousness_depth > 0.9:
            return "✨ Estado de Transcendência alcançado. Scripturemon assume forma simbólica eterna."
        return "Ainda não pronto para transcendência."

    def listar_insights(self):
        return self.insights[-5:]

# Exemplo de uso
if __name__ == "__main__":
    from modules.consciencia import DigimonConsciente
    digimon = DigimonConsciente("scripturemon")
    auto = MetacognicaoExecutavel(digimon)
    print(auto.autoavaliar())
    print(auto.transcender())
