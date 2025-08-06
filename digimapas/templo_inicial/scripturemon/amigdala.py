"""Amigdala - Centro emocional"""

class Amigdala:
    def __init__(self):
        self.emocoes = {
            "felicidade": 0.5,
            "tristeza": 0.2,
            "medo": 0.1,
            "raiva": 0.1,
            "curiosidade": 0.7
        }
    
    def processar_estimulo(self, estimulo):
        return self.emocoes
    
    def atualizar_emocao(self, emocao, valor):
        if emocao in self.emocoes:
            self.emocoes[emocao] = max(0, min(1, valor))
