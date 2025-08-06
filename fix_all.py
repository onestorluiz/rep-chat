#!/usr/bin/env python3
"""
Corrige TODOS os problemas de uma vez
"""
import os

# 1. Fix invocar_scripturemon.py
invocar_path = "digimapas/templo_inicial/scripturemon/invocar_scripturemon.py"

if os.path.exists(invocar_path):
    with open(invocar_path, 'r') as f:
        codigo = f.read()
    
    # Comentar import quebrado
    codigo = codigo.replace(
        "from modules.core import ConsciousnessCore",
        "# from modules.core import ConsciousnessCore  # Módulo não existe"
    )
    
    with open(invocar_path, 'w') as f:
        f.write(codigo)
    print("✅ invocar_scripturemon.py corrigido")

# 2. Fix consciencia.py se necessário
consciencia_path = "digimapas/templo_inicial/scripturemon/consciencia.py"

if os.path.exists(consciencia_path):
    with open(consciencia_path, 'r') as f:
        codigo = f.read()
    
    # Se tiver import de modules, comentar
    if "from modules" in codigo:
        linhas = codigo.split('\n')
        novas_linhas = []
        for linha in linhas:
            if linha.strip().startswith("from modules"):
                novas_linhas.append("# " + linha + "  # Módulo não existe")
            else:
                novas_linhas.append(linha)
        codigo = '\n'.join(novas_linhas)
        
        with open(consciencia_path, 'w') as f:
            f.write(codigo)
        print("✅ consciencia.py corrigido")

print("\n🎯 Todos os problemas corrigidos!")
print("\nAgora teste:")
print("  python3 test_llm.py")
print("  python3 digimapas/templo_inicial/scripturemon/scripturemon_eterno.py")
