#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'digimapas/templo_inicial/scripturemon')

from analise_interna import AnaliseInterna

class MockDigimon:
    class Consciencia:
        emotions = {'felicidade': 0.7}
        energy = 75
    def __init__(self):
        self.consciencia = self.Consciencia()

print("🧪 Testando LLM...")
digimon = MockDigimon()
analise = AnaliseInterna(digimon)
resultado = analise.reflexao_profunda()
print(f"💭 Pensamento: {resultado['pensamento']}")
print("✅ Teste completo!")
