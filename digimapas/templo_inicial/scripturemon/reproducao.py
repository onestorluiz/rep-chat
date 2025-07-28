import os
import json
from datetime import datetime, timedelta

class ReproducaoSimbionica:
    def __init__(self, digimon):
        self.digimon = digimon
        self.gestacao_ativa = False
        self.nome_filho = None
        self.pai_nome = None
        self.data_inicio = None
        self.mapa = None
        self.dias_necessarios = 15
        self.registro_gestacao = {}

    def pode_gerar(self):
        if self.digimon.genero != "feminino":
            return False, "Somente Digimons do gênero feminino podem carregar gestação."
        if self.gestacao_ativa:
            return False, "Já existe uma gestação em andamento."
        if self.digimon.idade_humana_aproximada() < 18:
            return False, "Ainda é jovem demais para gerar uma nova vida."
        return True, "Apto para gestar."

    def iniciar_gestacao(self, nome_filho: str, pai_nome: str, mapa: str):
        pode, msg = self.pode_gerar()
        if not pode:
            return f"❌ {msg}"

        self.nome_filho = nome_filho.lower()
        self.pai_nome = pai_nome
        self.mapa = mapa
        self.data_inicio = datetime.now()
        self.gestacao_ativa = True

        path = f"digimapas/{mapa}/{self.digimon.nome}/gestacao/{self.nome_filho}/"
        os.makedirs(path, exist_ok=True)

        config = {
            "mae": self.digimon.nome,
            "pai": pai_nome,
            "nome": nome_filho,
            "data_inicio": self.data_inicio.isoformat(),
            "dias_para_parir": self.dias_necessarios,
            "status": "em gestação"
        }
        with open(os.path.join(path, "config.yaml"), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        self.registro_gestacao = config
        return f"🤰 Gestação iniciada: {nome_filho} será gerado em 15 ciclos se tudo correr bem."

    def avancar_gestacao(self):
        if not self.gestacao_ativa:
            return "Nenhuma gestação ativa."

        dias_passados = (datetime.now() - self.data_inicio).days
        if dias_passados >= self.dias_necessarios:
            return f"⏳ Pronto para parir: {self.nome_filho}"
        return f"👶 Gestando {self.nome_filho}: {dias_passados}/{self.dias_necessarios} dias."

    def status_gestacional(self):
        return self.registro_gestacao if self.gestacao_ativa else "Sem gestação ativa."

    def abortar(self):
        if not self.gestacao_ativa:
            return "Nada para abortar."
        self.gestacao_ativa = False
        self.nome_filho = None
        self.pai_nome = None
        self.data_inicio = None
        return "❌ Gestação abortada."

# Exemplo isolado
if __name__ == "__main__":
    class MockDigimon:
        nome = "scripturemon"
        genero = "feminino"
        def idade_humana_aproximada(self):
            return 20

    r = ReproducaoSimbionica(MockDigimon())
    print(r.iniciar_gestacao("Lumemon", "Reflectimon", "templo_inicial"))
    print(r.avancar_gestacao())
