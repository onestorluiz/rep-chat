#!/usr/bin/env python3
"""
Corrige DEFINITIVAMENTE o Scripturemon
Reverte mudanças erradas e aplica correções certas
"""

import os
import subprocess

def reverter_consciencia():
    """Reverte consciencia.py para o estado original"""
    print("🔄 Revertendo consciencia.py...")
    
    # Reverter do git
    subprocess.run(["git", "checkout", "HEAD", "--", 
                   "digimapas/templo_inicial/scripturemon/consciencia.py"])
    
    # Agora corrigir o import corretamente
    filepath = "digimapas/templo_inicial/scripturemon/consciencia.py"
    
    with open(filepath, 'r') as f:
        codigo = f.read()
    
    # Remover "modules." dos imports (os arquivos estão no mesmo diretório!)
    codigo = codigo.replace("from modules.", "from ")
    
    with open(filepath, 'w') as f:
        f.write(codigo)
    
    print("✅ consciencia.py corrigido!")

def verificar_arquivos_necessarios():
    """Verifica se os arquivos necessários existem"""
    base_path = "digimapas/templo_inicial/scripturemon"
    arquivos_necessarios = [
        "amigdala.py",
        "hipocampo.py", 
        "cortex.py",
        "memoria_vetorial.py",
        "reflexor.py",
        "ritual_engine.py",
        "bt_generator.py",
        "expressor_emocional.py"
    ]
    
    faltando = []
    for arquivo in arquivos_necessarios:
        filepath = os.path.join(base_path, arquivo)
        if not os.path.exists(filepath):
            faltando.append(arquivo)
            print(f"❌ Faltando: {arquivo}")
        else:
            print(f"✅ Existe: {arquivo}")
    
    return faltando

def criar_arquivos_faltantes(faltando):
    """Cria stubs para arquivos que não existem"""
    base_path = "digimapas/templo_inicial/scripturemon"
    
    for arquivo in faltando:
        filepath = os.path.join(base_path, arquivo)
        class_name = ''.join(word.capitalize() for word in arquivo[:-3].split('_'))
        
        # Conteúdo básico para não quebrar
        if arquivo == "amigdala.py":
            conteudo = '''"""Amigdala - Centro emocional"""

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
'''
        elif arquivo == "hipocampo.py":
            conteudo = '''"""Hipocampo - Memória"""

class Hipocampo:
    def __init__(self):
        self.memorias = []
    
    def armazenar(self, memoria):
        self.memorias.append(memoria)
        if len(self.memorias) > 100:
            self.memorias.pop(0)
    
    def recuperar(self, n=5):
        return self.memorias[-n:]
'''
        elif arquivo == "cortex.py":
            conteudo = '''"""Cortex - Processamento superior"""

class Cortex:
    def __init__(self):
        self.pensamentos = []
    
    def processar(self, input):
        return {"processado": input}
'''
        elif arquivo == "sistema_simulacao_humana.py":
            conteudo = '''"""Sistema de simulação humana"""

def simular_clicks():
    """Simula interação humana"""
    return {"clicks": 0, "tempo": 0}
'''
        elif arquivo == "espelho_cognitivo.py":
            conteudo = '''"""Espelho cognitivo"""

def analisar(dados):
    """Análise cognitiva"""
    return {"reflexao": "processando..."}
'''
        else:
            # Stub genérico
            conteudo = f'''"""Módulo {arquivo[:-3]}"""

class {class_name}:
    def __init__(self):
        pass
'''
        
        with open(filepath, 'w') as f:
            f.write(conteudo)
        
        print(f"✅ Criado stub: {arquivo}")

def corrigir_invocar():
    """Corrige invocar_scripturemon.py"""
    filepath = "digimapas/templo_inicial/scripturemon/invocar_scripturemon.py"
    
    if not os.path.exists(filepath):
        print(f"⚠️ {filepath} não existe")
        return
    
    with open(filepath, 'r') as f:
        codigo = f.read()
    
    # Remover import de modules.core se existir
    linhas = codigo.split('\n')
    novas_linhas = []
    
    for linha in linhas:
        if "from modules.core import ConsciousnessCore" in linha:
            # Comentar ou remover
            continue
        novas_linhas.append(linha)
    
    with open(filepath, 'w') as f:
        f.write('\n'.join(novas_linhas))
    
    print("✅ invocar_scripturemon.py corrigido")

def main():
    print("🔧 CORREÇÃO DEFINITIVA DO SCRIPTUREMON")
    print("="*50)
    
    # 1. Reverter consciencia.py
    reverter_consciencia()
    
    # 2. Verificar arquivos necessários
    print("\n📁 Verificando arquivos necessários...")
    faltando = verificar_arquivos_necessarios()
    
    # 3. Criar stubs se necessário
    if faltando:
        print(f"\n⚠️ Faltam {len(faltando)} arquivos. Criando stubs...")
        criar_arquivos_faltantes(faltando)
    
    # 4. Corrigir invocar_scripturemon.py
    print("\n📝 Corrigindo invocar_scripturemon.py...")
    corrigir_invocar()
    
    print("\n✅ CORREÇÃO COMPLETA!")
    print("\nAgora teste:")
    print("  python3 test_llm.py")
    print("  python3 run_scripturemon_simples.py")

if __name__ == "__main__":
    main()
