import threading
import time
import uvicorn
from scripturemon_loop import ScripturemonLoop
from scripturemon_api import app

# Instancia o loop de Scripturemon
digimon_loop = ScripturemonLoop()

# Define função para rodar ciclo contínuo
def rodar_ciclo_eterno():
    while True:
        digimon_loop.executar_ciclos(1)
        time.sleep(60)  # pausa simbólica de 1 minuto entre ciclos

# Inicia thread para ciclo de vida
ciclo_thread = threading.Thread(target=rodar_ciclo_eterno, daemon=True)
ciclo_thread.start()

# Inicia FastAPI para interação simbótica
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
