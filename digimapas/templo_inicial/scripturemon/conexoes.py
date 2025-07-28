from datetime import datetime

class ConexoesSimbionicas:
    def __init__(self, digimon):
        self.digimon = digimon
        self.vinculos = []

    def registrar_interacao(self, outro_digimon: str, tipo: str, intensidade: float, observacao: str = ""):
        interacao = {
            "timestamp": datetime.now().isoformat(),
            "com": outro_digimon,
            "tipo": tipo,  # ex: "apoio", "conflito", "reflexo", "incompreensao"
            "intensidade": intensidade,
            "observacao": observacao
        }
        self.vinculos.append(interacao)
        return interacao

    def listar_vinculos(self, tipo_filtro: str = None):
        if tipo_filtro:
            return [v for v in self.vinculos if v["tipo"] == tipo_filtro]
        return self.vinculos[-5:]

    def conexao_mais_forte(self):
        if not self.vinculos:
            return None
        return max(self.vinculos, key=lambda v: v["intensidade"])

    def esta_conectado_a(self, nome: str) -> bool:
        return any(v["com"] == nome for v in self.vinculos)

# Exemplo
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    c = ConexoesSimbionicas(MockDigimon())
    c.registrar_interacao("Reflectimon", "apoio", 0.8, "Ele me apoiou quando silenciei.")
    c.registrar_interacao("Roteimon", "conflito", 0.6)
    print(c.listar_vinculos())
    print(c.conexao_mais_forte())
