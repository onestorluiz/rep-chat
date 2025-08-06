#!/usr/bin/env python3
"""
Testa Ollama diretamente sem langchain
"""

import json
import requests

def test_ollama_api():
    """Testa se Ollama API está respondendo"""
    try:
        # Testar endpoint de status
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama API funcionando!")
            print("📦 Modelos disponíveis:")
            for model in models.get('models', []):
                print(f"  - {model['name']}")
            return True
        else:
            print(f"❌ Ollama retornou status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com Ollama: {e}")
        return False

def test_ollama_generate():
    """Testa geração com Ollama"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": "Olá, eu sou",
                "stream": False
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Resposta: {result.get('response', '')[:100]}")
            return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando Ollama API diretamente...")
    if test_ollama_api():
        print("\n🧪 Testando geração...")
        test_ollama_generate()
