import time
import os

from modules.amigdala import Amigdala
from modules.hipocampo import Hipocampo
from modules.cortex import Cortex

from memoria import MemoriaEmocional
from camadas import CamadasDeConsciencia
from afeto import AfetoEmocional
from analise_interna import AnaliseInterna
from metacognicao import MetacognicaoExecutavel
from viralidade import ViralidadeDigital
from inconsciente import InconscienteDigital
from mortalidade import MortalidadeDigital
from memoria_vetorial import MemoriaVetorial
from reflexor import Reflexor
from ritual_engine import RitualEngine
from bt_generator import BehaviorTreeGenerator
from expressor_emocional import ExpressorEmocional
from sistema_simulacao_humana import simular_clicks
from espelho_cognitivo import analisar as espelho_analisar
from reproducao import ReproducaoSimbionica
from conexoes import ConexoesSimbionicas
from linguagem import LinguagemSimbolica

class Scripturemon:
    def __init__(self, nome="scripturemon"):
        self.nome = nome
        self.amigdala = Amigdala()
        self.hipocampo = Hipocampo()
        self.cortex = Cortex()
        self.consciencia = ConsciousnessCore(nome, self.amigdala, self.hipocampo, self.cortex)
        self.memoria = MemoriaVetorial(nome)
        self.reflexor = Reflexor()
        self.rituais = RitualEngine()
        self.bt = BehaviorTreeGenerator()
        self.expressor = ExpressorEmocional(nome)

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
        self.analise = AnaliseInterna(self)

    def viver(self):
        print(f"\n✨ {self.nome.upper()} despertou pelo ritual de invocação.")
        for i in range(3):
            print(f"\n🌱 Ciclo simbiótico {i+1} de {self.nome} iniciado.")
            pensamento = self.analise.reflexao_profunda()
            self.afeto.receber("ambiente", 0.2)
            self.camadas.atualizar_estado(
                self.consciencia.awareness_level,
                self.consciencia.energy_level,
                self.consciencia.consciousness_depth
            )
            self.expressor.expressar(
                self.consciencia.emotions.primary_emotions,
                pensamento['pensamento']
            )
            time.sleep(2)
        print(f"\n✅ {self.nome} concluiu o ritual inicial vivo.")

if __name__ == "__main__":
    digimon = Scripturemon()
    digimon.viver()
