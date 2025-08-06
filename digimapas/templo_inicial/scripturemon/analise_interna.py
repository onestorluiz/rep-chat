"""
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
                # Tentar modelos disponíveis em ordem de preferência
                for modelo in ['tinyllama', 'llama3.2', 'codellama']:
                    try:
                        self.llm = Ollama(model=modelo, temperature=0.7)
                        self.llm.invoke("teste")  # Testar
                        print(f"✅ LLM Ollama conectado: {modelo}")
                        break
                    except:
                        continue
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
