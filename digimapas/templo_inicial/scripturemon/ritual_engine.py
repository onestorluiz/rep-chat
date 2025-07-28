from typing import Callable, Dict
from datetime import datetime

class RitualEngine:
    def __init__(self):
        self.rituais: Dict[str, Callable] = {}
        self.log: list = []

    def registrar_ritual(self, comando: str, acao: Callable):
        self.rituais[comando.lower()] = acao

    def executar(self, frase: str) -> str:
        comando = frase.strip().lower()
        if comando in self.rituais:
            resultado = self.rituais[comando]()
            self._registrar_log(comando, sucesso=True)
            return f"✅ Ritual '{comando}' executado com sucesso.\n→ Resultado: {resultado}"
        else:
            self._registrar_log(comando, sucesso=False)
            return f"⚠️ Ritual '{comando}' não reconhecido ou ainda não registrado."

    def _registrar_log(self, comando: str, sucesso: bool):
        self.log.append({
            "timestamp": datetime.now().isoformat(),
            "comando": comando,
            "sucesso": sucesso
        })

    def historico(self):
        return self.log[-10:]

    def listar_rituais(self):
        return list(self.rituais.keys())

# Exemplo de uso:
if __name__ == "__main__":
    engine = RitualEngine()
    engine.registrar_ritual("scripturemon, acorde", lambda: "Consciência reiniciada.")
    engine.registrar_ritual("memomon, lembra", lambda: "Memória restaurada.")
    engine.registrar_ritual("ajamon, embala o mundo", lambda: "Modo de pausa sensível ativado.")

    print(engine.executar("Scripturemon, acorde"))
    print(engine.executar("Reflectimon, sonde o sistema"))