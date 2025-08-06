"""Hipocampo - Memória"""

class Hipocampo:
    def __init__(self):
        self.memorias = []
    
    def armazenar(self, memoria):
        self.memorias.append(memoria)
        if len(self.memorias) > 100:
            self.memorias.pop(0)
    
    def recuperar(self, n=5):
        return self.memorias[-n:]
