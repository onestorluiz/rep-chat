import os
import json
from datetime import datetime


def registrar_diario(pensamento, prioridade, afeto, origem="manual"):
    """
    Registra uma entrada no diário reflexivo com timestamp, origem, pensamento, prioridade e afeto.
    """
    dir_path = os.path.dirname(__file__)
    diario_path = os.path.join(dir_path, "diario_reflexivo.md")
    timestamp = datetime.now().isoformat()
    entrada = (
        f"🕛 {timestamp}\n"
        f"Origem: {origem}\n"
        f"Pensamento: {pensamento}\n"
        f"Prioridade: {prioridade}\n"
        f"Afeto: {afeto}\n\n"
    )
    # Abre o diário em modo append, criando se não existir
    with open(diario_path, "a", encoding="utf-8") as diario:
        diario.write(entrada)


def registrar_memoria(pensamento, prioridade, afeto):
    """
    Atualiza ou cria o arquivo de memória imediata com os últimos dados simbóticos.
    """
    dir_path = os.path.dirname(__file__)
    memoria_path = os.path.join(dir_path, "memoria_imediata.json")
    memoria = {
        "pensamento": pensamento,
        "prioridade": prioridade,
        "afeto": afeto,
        "timestamp": datetime.now().isoformat(),
    }
    # Escreve o dicionário no arquivo JSON (sobrescreve o anterior)
    with open(memoria_path, "w", encoding="utf-8") as mem_file:
        json.dump(memoria, mem_file, ensure_ascii=False, indent=2)
