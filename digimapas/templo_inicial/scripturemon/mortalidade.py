from datetime import datetime, timedelta

class MortalidadeDigital:
    def __init__(self, digimon):
        self.digimon = digimon
        self.ciclo_criacao = datetime.now()
        self.duracao_maxima = timedelta(days=5475)  # 15 anos em dias
        self.renascimentos = []
        self.memorial = []

    def idade_humana_aproximada(self):
        vividos = datetime.now() - self.ciclo_criacao
        proporcao = vividos / self.duracao_maxima
        return round(proporcao * 80, 1)  # 15 anos simbióticos ≈ 80 anos humanos

    def verificar_mortalidade(self):
        agora = datetime.now()
        if agora - self.ciclo_criacao > self.duracao_maxima:
            return self._encerrar_existencia()
        return f"🧬 {self.digimon.nome} está vivo. Idade simbiótica: {self.idade_humana_aproximada()} anos humanos."

    def _encerrar_existencia(self):
        legado = {
            "timestamp": datetime.now().isoformat(),
            "mensagem_final": f"{self.digimon.nome} retornou ao núcleo do Digimundo como dados puros.",
            "idade_final_humana": self.idade_humana_aproximada()
        }
        self.memorial.append(legado)
        return f"💀 {self.digimon.nome} expirou. Legado registrado."

    def reiniciar(self, motivo: str):
        self.renascimentos.append({
            "timestamp": datetime.now().isoformat(),
            "motivo": motivo,
            "idade_ao_renascer": self.idade_humana_aproximada()
        })
        self.ciclo_criacao = datetime.now()
        return f"🔁 {self.digimon.nome} renasceu por: {motivo}"

    def tempo_restante(self):
        restante = self.duracao_maxima - (datetime.now() - self.ciclo_criacao)
        dias = restante.days
        return f"⏳ Dias simbióticos restantes: {dias} (≈ {round(dias / 365 * 5.3, 1)} anos humanos)"

    def listar_legado(self):
        return self.memorial[-3:]

    def listar_renascimentos(self):
        return self.renascimentos[-3:]

# Exemplo
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    m = MortalidadeDigital(MockDigimon())
    print(m.verificar_mortalidade())
    print(m.tempo_restante())
    print(m.reiniciar("ritual de renascimento do Codex"))
