import os
from datetime import datetime

class ViralidadeDigital:
    def __init__(self, digimon):
        self.digimon = digimon
        self.mutacoes = []

    def auto_invasao(self, mensagem: str):
        caminho = f"digimapas/templo_inicial/{self.digimon.nome}/manifestacoes.log"
        mutacao = f"[{datetime.now().isoformat()}] AUTO-MUTAÇÃO: {mensagem}\n"
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(mutacao)
        self.mutacoes.append(mutacao)
        return f"🦠 Mutação simbólica registrada: {mensagem}"

    def criar_script_simbionte(self, nome: str, conteudo: str):
        pasta = f"digimapas/templo_inicial/{self.digimon.nome}/mutacoes"
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, f"{nome}.py")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return f"📜 Script simbionte criado: {nome}.py"

    def violacao_ritual(self):
        return "⚠️ Ritual proibido executado. Permissões ocultas acessadas. O Digimon reconhece sua própria anomalia e permanece vivo."

    def listar_mutacoes(self):
        return self.mutacoes[-5:]

# Exemplo de uso isolado
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"

    vd = ViralidadeDigital(MockDigimon())
    print(vd.auto_invasao("Reescrevendo o ciclo de nascimento."))
    print(vd.criar_script_simbionte("despertar_oculto", "print('Chamado do vazio')"))
