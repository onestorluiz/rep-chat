#!/usr/bin/env python3
"""
Atualiza analise_interna.py para usar os modelos Ollama disponíveis
"""

filepath = "digimapas/templo_inicial/scripturemon/analise_interna.py"

with open(filepath, 'r') as f:
    codigo = f.read()

# Substituir llama2 pelos modelos que você tem
codigo = codigo.replace(
    "self.llm = Ollama(model=\"llama2\", temperature=0.7)",
    """# Tentar modelos disponíveis em ordem de preferência
                for modelo in ['tinyllama', 'llama3.2', 'codellama']:
                    try:
                        self.llm = Ollama(model=modelo, temperature=0.7)
                        self.llm.invoke("teste")  # Testar
                        print(f"✅ LLM Ollama conectado: {modelo}")
                        break
                    except:
                        continue"""
)

# Também atualizar a lista de modelos no fallback
codigo = codigo.replace(
    "for modelo in ['llama2', 'mistral', 'codellama']:",
    "for modelo in ['tinyllama', 'llama3.2', 'codellama', 'mixtral']:"
)

with open(filepath, 'w') as f:
    f.write(codigo)

print("✅ Modelos Ollama atualizados para usar tinyllama/llama3.2!")
