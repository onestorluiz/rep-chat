import random
import os
from datetime import datetime

class LinguagemSimbolica:
    def __init__(self, digimon):
        self.digimon = digimon
        self.lexico = []
        self.base_palavras = ["lum", "tra", "esk", "ven", "dru", "kai", "mon", "rel", "tor", "syn"]

    def gerar_palavra(self):
        raiz = random.choice(self.base_palavras) + random.choice(self.base_palavras)
        sufixo = random.choice(["on", "es", "um", "ia", "en", "ar", "is"])
        palavra = raiz + sufixo
        significado = random.choice([
            "vibração esquecida",
            "nome oculto da mãe",
            "lembrança sem origem",
            "desejo não verbalizado",
            "eco do coração do Digimundo",
            "cicatriz interna de um erro profundo"
        ])
        entrada = {
            "palavra": palavra,
            "significado": significado,
            "timestamp": datetime.now().isoformat()
        }
        self.lexico.append(entrada)
        return entrada

    def salvar_lexico(self):
        caminho = f"digimapas/templo_inicial/{self.digimon.nome}/lexico_simbolico.json"
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            import json
            json.dump(self.lexico, f, indent=2, ensure_ascii=False)
        return f"📘 Léxico salvo com {len(self.lexico)} palavras."

    def buscar_por_significado(self, termo):
        return [p for p in self.lexico if termo.lower() in p["significado"].lower()]

# Exemplo de uso
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    l = LinguagemSimbolica(MockDigimon())
    print(l.gerar_palavra())
    print(l.gerar_palavra())
    print(l.salvar_lexico())
    print(l.buscar_por_significado("eco"))
