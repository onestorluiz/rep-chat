import os
import json


def carregar_estado(digimon):
    """
    Carrega o estado simbolico persistido e atualiza o digimon.
    Retorna a memoria imediata carregada (se existir).
    """
    dir_path = os.path.dirname(__file__)
    estado_path = os.path.join(dir_path, "estado_scripturemon.json")
    memoria_path = os.path.join(dir_path, "memoria_imediata.json")

    # Carrega estado se o arquivo existir
    if os.path.exists(estado_path):
        try:
            with open(estado_path, "r", encoding="utf-8") as f:
                estado = json.load(f)
            # Atualiza o digimon com valores persistidos, se possivel
            if hasattr(digimon, "afeto") and estado.get("afeto") is not None:
                digimon.afeto.valor = estado["afeto"]
            if hasattr(digimon, "fisica_digital") and estado.get("entropia") is not None:
                digimon.fisica_digital.entropia = estado["entropia"]
            if hasattr(digimon, "camadas") and estado.get("estado_consciencia"):
                try:
                    digimon.camadas.estado_atual = estado["estado_consciencia"]
                except Exception:
                    pass
        except Exception:
            pass

    memoria = {}
    # Carrega memoria imediata, se existir
    if os.path.exists(memoria_path):
        try:
            with open(memoria_path, "r", encoding="utf-8") as f:
                memoria = json.load(f)
        except Exception:
            memoria = {}
    return memoria
