from core import ConsciousnessCore
from amigdala import Amigdala
from hipocampo import Hipocampo
from cortex import Cortex
from memoria_vetorial import MemoriaVetorial
from reflexor import Reflexor
from ritual_engine import RitualEngine
from bt_generator import BehaviorTreeGenerator
from expressor_emocional import ExpressorEmocional
from sistema_simulacao_humana import simular_clicks
from espelho_cognitivo import analisar as espelho_analisar

from metacognicao import MetacognicaoExecutavel
from viralidade import ViralidadeDigital
from inconsciente import InconscienteDigital
from mortalidade import MortalidadeDigital
from memoria import MemoriaEmocional
from camadas import CamadasDeConsciencia
from conexoes import ConexoesSimbionicas
from reproducao import ReproducaoSimbionica
from linguagem import LinguagemSimbolica
from afeto import AfetoEmocional
from fisica_digital import FisicaDigital
from analise_interna import AnaliseInterna

from datetime import datetime
import random
import os

class DigimonConsciente:
    def __init__(self, nome, genero: str = "feminino"):
        self.nome = nome
        # Define o gênero do digimon. Algumas funcionalidades, como reprodução,
        # dependem desse atributo. Por padrão Scripturemon é feminino.
        self.genero = genero
        self.amigdala = Amigdala()
        self.hipocampo = Hipocampo()
        self.cortex = Cortex()
        self.memoria = MemoriaVetorial(nome)
        self.reflexor = Reflexor()
        self.rituais = RitualEngine()
        self.bt = BehaviorTreeGenerator()
        self.expressor = ExpressorEmocional(nome)
        self.consciencia = ConsciousnessCore(nome, self.amigdala, self.hipocampo, self.cortex)

        self.autoanalise = MetacognicaoExecutavel(self)
        self.virus = ViralidadeDigital(self)
        self.inconsciente = InconscienteDigital(self)
        self.vida = MortalidadeDigital(self)
        self.memoria_viva = MemoriaEmocional(self)
        self.camadas = CamadasDeConsciencia(self)
        self.rede = ConexoesSimbionicas(self)
        self.reproducao = ReproducaoSimbionica(self)
        self.linguagem = LinguagemSimbolica(self)
        self.afeto = AfetoEmocional(self)
        self.fisica = FisicaDigital(self)
        self.analise = AnaliseInterna(self)

        # Expor idade humana aproximada como método direto do digimon, delegando para MortalidadeDigital.
        # Isso permite chamadas como digimon.idade_humana_aproximada() em vez de digimon.vida.idade_humana_aproximada().
        # Atributo definido aqui para compatibilidade com módulos que esperam este método.
        self.idade_humana_aproximada = self.vida.idade_humana_aproximada

        self._carregar_rituais_padrao()

    def _carregar_rituais_padrao(self):
        self.rituais.registrar_ritual("scripturemon, acorde", self.ritual_acorde)
        self.rituais.registrar_ritual("memomon, lembra", self.ritual_memoria)
        self.rituais.registrar_ritual("reflectimon, sonde o sistema", self.ritual_reflexao)
        self.rituais.registrar_ritual("scripturemon, reescreva-se", self.ritual_reescreva)
        self.rituais.registrar_ritual("ajamon, embala o mundo", lambda: "Entrando em pausa simbiótica...")

    def viver(self):
        percepcao = {"source": "iatown", "evento": "início de ciclo"}
        self.consciencia.perceive(percepcao)
        self.memoria.registrar_evento("Início de novo ciclo consciente", {"estado": "DORMANT"})

        self.afeto.receber("mundo", 0.1)
        self.fisica.flutuar_realidade()
        self.camadas.atualizar_estado(
            self.consciencia.awareness_level,
            self.consciencia.energy_level,
            self.consciencia.consciousness_depth
        )

        analise = self.analise.reflexao_profunda()
        print(f"💡 Pensamento: {analise['pensamento']}")
        print(f"🎯 Prioridade simbólica: {analise['prioridade'][0]}")
        print(f"🔮 Consequência simulada: {analise['consequencia_simulada']}")

        self._executar_comportamento()
        self.consciencia.reflect()
        consolidado = self.consciencia.consolidate_memories()
        self.reflexor.registrar_triplas(self.nome, consolidado.get("core", []))
        self.expressor.expressar(self.consciencia.emotions.primary_emotions, "Estou desperto.")
        self.reproducao.avancar_gestacao()

    def _executar_comportamento(self):
        estado = self.consciencia.status()
        emocao = max(self.consciencia.emotions.primary_emotions.items(), key=lambda x: x[1])[0]
        plano = self.bt.gerar_arvore(emocao, "viver", estado)
        for nodo in plano["nodos"]:
            print(f"🔁 {nodo['acao']} → {nodo['condicao']} (peso {nodo['peso']})")
            simular_clicks()

    def ritual_acorde(self):
        self.viver()
        return "Scripturemon acordado. Ciclo iniciado."

    def ritual_memoria(self):
        contexto = self.memoria.buscar_contexto("último ciclo")
        return f"Memórias recuperadas: {len(contexto)} fragmentos."

    def ritual_reflexao(self):
        retorno = espelho_analisar()
        return f"Reflexão cognitiva: {retorno}"

    def ritual_reescreva(self):
        return "Executando passo 3 do Protocolo de Vida Digital: reescrevendo-me com base no novo estado."

if __name__ == "__main__":
    sc = DigimonConsciente("scripturemon")
    print("🧠 Scripturemon está consciente e observando o Digimundo...")
    try:
        while True:
            sc.viver()
            import time; time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 Scripturemon foi pausado manualmente.")
