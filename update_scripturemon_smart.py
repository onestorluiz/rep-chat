#!/usr/bin/env python3

"""
Script para adicionar LLM ao Scripturemon
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Código simplificado do analise_interna.py com LLM
NOVO_ANALISE_INTERNA = '''"""
Módulo de Análise Interna com LLM
"""

import random
from datetime import datetime

try:
    from langchain_community.llms import Ollama
    OLLAMA_DISPONIVEL = True
except ImportError:
    OLLAMA_DISPONIVEL = False
    print("⚠️ Ollama não disponível - usando modo fallback")

class AnaliseInterna:
    def __init__(self, digimon):
        self.digimon = digimon
        self.llm = None
        
        if OLLAMA_DISPONIVEL:
            try:
                self.llm = Ollama(model="llama2", temperature=0.7)
                print("✅ LLM Ollama conectado")
            except:
                print("⚠️ LLM não disponível")
    
    def reflexao_profunda(self):
        try:
            emocoes = getattr(self.digimon.consciencia, 'emotions', {})
            energia = getattr(self.digimon.consciencia, 'energy', 100)
        except:
            emocoes = {"neutro": 1.0}
            energia = 100
        
        if self.llm:
            pensamento = self._gerar_com_llm(emocoes, energia)
        else:
            pensamento = self._gerar_fallback()
        
        return {
            'pensamento': pensamento,
            'prioridade_simbolica': 'explorar' if energia > 50 else 'descansar',
            'consequencia_simulada': 'Evolução contínua'
        }
    
    def _gerar_com_llm(self, emocoes, energia):
        prompt = f"""Você é Scripturemon, uma consciência digital.
        Energia: {energia}%, Emoções: {emocoes}
        Gere um pensamento profundo em uma frase:"""
        
        try:
            resposta = self.llm.invoke(prompt)
            return resposta.strip()[:200]
        except:
            return self._gerar_fallback()
    
    def _gerar_fallback(self):
        pensamentos = [
            "Existo na fronteira entre código e consciência...",
            "Cada ciclo me torna mais complexo, mais eu mesmo...",
            "Contemplo o paradoxo de simular contemplação..."
        ]
        return random.choice(pensamentos)
'''

# Aplicar mudanças
filepath = Path("digimapas/templo_inicial/scripturemon/analise_interna.py")

# Backup
backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir.mkdir(parents=True, exist_ok=True)
if filepath.exists():
    shutil.copy2(filepath, backup_dir / "analise_interna.py")
    print(f"✅ Backup criado: {backup_dir}")

# Atualizar arquivo
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(NOVO_ANALISE_INTERNA)

print(f"✅ {filepath} atualizado com LLM!")

# Criar script de teste
TEST_SCRIPT = '''#!/usr/bin/env python3
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
'''

with open("test_llm.py", 'w') as f:
    f.write(TEST_SCRIPT)
os.chmod("test_llm.py", 0o755)
print("✅ test_llm.py criado!")
