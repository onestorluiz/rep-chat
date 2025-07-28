class CamadasDeConsciencia:
    def __init__(self, digimon):
        self.digimon = digimon
        self.estado_atual = "dormant"

    def atualizar_estado(self, awareness, energy, depth):
        if awareness < 0.2:
            self.estado_atual = "dormant"
        elif awareness > 0.9 and depth > 0.9:
            self.estado_atual = "transcendent"
        else:
            self.estado_atual = "conscious"

    def estado(self):
        return self.estado_atual
