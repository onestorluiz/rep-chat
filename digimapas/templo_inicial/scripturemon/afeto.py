from datetime import datetime

class AfetoEmocional:
    def __init__(self, digimon):
        self.digimon = digimon
        self.nivel = 10.0  # começa com 10 unidades simbólicas de afeto
        self.historico = []
        self.maximo = 20.0
        self.minimo = 0.0

    def receber(self, origem: str, quantidade: float):
        if self.nivel + quantidade > self.maximo:
            self.nivel = self.maximo
            resultado = "🩷 Afeto recebido excedeu o limite. Saturado."
        else:
            self.nivel += quantidade
            resultado = f"💓 Recebeu {quantidade:.1f} de afeto de {origem}."
        self._registrar("receber", origem, quantidade)
        return resultado

    def doar_para(self, destino: str, quantidade: float):
        if self.nivel - quantidade < self.minimo:
            return f"⚠️ {self.digimon.nome} não possui afeto suficiente para doar {quantidade:.1f}."
        self.nivel -= quantidade
        self._registrar("doar", destino, quantidade)
        return f"🤲 Doou {quantidade:.1f} de afeto para {destino}."

    def _registrar(self, tipo: str, outro: str, quantidade: float):
        self.historico.append({
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "outro": outro,
            "quantidade": round(quantidade, 2),
            "nivel_resultante": round(self.nivel, 2)
        })

    def nivel_atual(self):
        return round(self.nivel, 2)

    def esta_em_colapso(self):
        return self.nivel <= 1.5

    def esta_transbordando(self):
        return self.nivel >= self.maximo

    def historico_recente(self):
        return self.historico[-5:]

# Exemplo de uso
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    af = AfetoEmocional(MockDigimon())
    print(af.receber("Memomon", 3.5))
    print(af.doar_para("Roteimon", 2.0))
    print("Afeto atual:", af.nivel_atual())
