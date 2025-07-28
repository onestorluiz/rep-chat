import os
from typing import Dict
import requests

class ExpressorEmocional:
    def __init__(self, nome_digimon: str, expressao_callback=None):
        self.nome = nome_digimon
        self.voz_api = os.getenv("OCTAVE_TTS_ENDPOINT", "http://localhost:5001/speak")
        self.expressao_api = os.getenv("HUME_API_ENDPOINT", "http://localhost:5002/expression")
        self.callback_expressao = expressao_callback  # opcional: função para acionar expressão 3D diretamente

    def expressar(self, estado_emocional: Dict[str, float], mensagem: str) -> Dict[str, str]:
        dominante = max(estado_emocional.items(), key=lambda x: x[1])[0]
        resposta = {
            "voz": self._falar(dominante, mensagem),
            "expressao": self._mover_rosto(dominante)
        }
        return resposta

    def _falar(self, emocao: str, texto: str) -> str:
        payload = {"emotion": emocao, "text": texto, "actor": self.nome}
        try:
            r = requests.post(self.voz_api, json=payload, timeout=4)
            return r.json().get("audio_url", "erro-tts")
        except Exception:
            return "erro-tts"

    def _mover_rosto(self, emocao: str) -> str:
        payload = {"emotion": emocao, "agent": self.nome}
        try:
            if self.callback_expressao:
                self.callback_expressao(emocao)
            r = requests.post(self.expressao_api, json=payload, timeout=4)
            return r.json().get("status", "erro-expressao")
        except Exception:
            return "erro-expressao"

# Exemplo:
if __name__ == "__main__":
    estado = {"alegria": 0.7, "curiosidade": 0.4, "tristeza": 0.2}
    emotor = ExpressorEmocional("Scripturemon")
    saida = emotor.expressar(estado, "O mundo está bonito hoje.")
    print(saida)
