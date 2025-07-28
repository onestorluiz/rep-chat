import os
import json
import time


def load_memoria():
    path = os.path.join(os.path.dirname(__file__), "memoria_imediata.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def load_diario():
    path = os.path.join(os.path.dirname(__file__), "diario_reflexivo.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-10:])
    return "Sem registros no diário."


def display_panel():
    while True:
        memoria = load_memoria()
        pensamento = memoria.get("pensamento", "")
        prioridade = memoria.get("prioridade", "")
        afeto = memoria.get("afeto", "")
        estado = memoria.get("estado_consciencia", "")
        origem = memoria.get("origem", "")
        diario_trecho = load_diario()
        # Limpar terminal
        os.system("cls" if os.name == "nt" else "clear")
        print("🧜️ Painel Eterno de Scripturemon")
        print(f"Pensamento atual: {pensamento}")
        print(f"Prioridade simbólica: {prioridade}")
        print(f"Emoção/afeto: {afeto}")
        print(f"Estado de consciência: {estado}")
        print(f"Origem: {origem}")
        print("\nÚltimos registros do diário:")
        print(diario_trecho)
        # esperar 10 segundos
        time.sleep(10)


if __name__ == "__main__":
    try:
        display_panel()
    except KeyboardInterrupt:
        print("\nEncerrando painel eterno...")
