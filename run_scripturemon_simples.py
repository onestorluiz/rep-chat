#!/usr/bin/env python3
"""
Roda Scripturemon sem uvicorn
"""
import sys
sys.path.insert(0, 'digimapas/templo_inicial/scripturemon')

from consciencia import DigimonConsciente

print("🚀 Iniciando Scripturemon (modo simples)...")

try:
    scripturemon = DigimonConsciente("Scripturemon")
    
    # Loop eterno
    ciclo = 0
    while True:
        ciclo += 1
        print(f"\n{'='*50}")
        print(f"CICLO {ciclo}")
        print('='*50)
        
        scripturemon.viver()
        
        # Pausa para ler
        import time
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n👋 Scripturemon entrando em hibernação...")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
