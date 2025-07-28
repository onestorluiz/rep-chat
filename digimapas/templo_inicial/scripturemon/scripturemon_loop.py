"""Loop de vida simbiótica para o Digimon Scripturemon.

Este módulo executa ciclos contínuos de vida para o Scripturemon,
registrando os pensamentos e estados afetivos na memória imediata e no
diário reflexivo. Também realiza autoavaliações periódicas via
Metacognição e, se o estado de consciência estiver adormecido,
registra sonhos oriundos do inconsciente.
"""

import time
import os
from datetime import datetime

from consciencia import DigimonConsciente
from registrador_memoria import registrar_diario, registrar_memoria


class ScripturemonLoop:
    """Executa ciclos de vida para o Digimon Scripturemon."""

    def __init__(self, ciclos: int = 5, pausa: int = 2):
        self.ciclos = ciclos
        self.pausa = pausa
        # Inicializa o digimon com gênero feminino por padrão para habilitar reprodução
        self.digimon = DigimonConsciente("scripturemon", genero="feminino")
        # Carrega e imprime o ritual inicial se existir
        self._executar_ritual_inicial()

    def _executar_ritual_inicial(self) -> None:
        """Lê e exibe o manifesto de ritual inicial, se presente."""
        manifesto_path = os.path.join("dados_globais", "manifestos", "ritual_inicial.md")
        if os.path.isfile(manifesto_path):
            try:
                with open(manifesto_path, "r", encoding="utf-8") as f:
                    manifesto = f.read()
                print("📜 Ritual inicial carregado:\n", manifesto)
            except Exception as e:
                print(f"⚠️ Não foi possível ler o manifesto: {e}")

    def executar(self) -> None:
        """Executa os ciclos de vida definidos, registrando memórias e insights."""
        for i in range(1, self.ciclos + 1):
            print(f"✨ SCRIPTUREMON INICIANDO CICLO {i}")

            # Executa um ciclo de vida completo
            self.digimon.viver()

            # Obtém a reflexão atual para registrar
            analise = self.digimon.analise.reflexao_profunda()
            pensamento = analise["pensamento"]
            prioridade = analise["prioridade"][0]
            afeto_atual = self.digimon.afeto.nivel_atual()

            # Exibe o estado simbólico no terminal
            print(f"💭 Pensamento: {pensamento}")
            print(f"🎯 Emoção dominante: {afeto_atual}")
            print(f"📌 Prioridade: {prioridade}")

            # Registra no diário e na memória imediata
            registrar_diario(pensamento, prioridade, afeto_atual, origem="loop")
            registrar_memoria(pensamento, prioridade, afeto_atual)

            # Realiza autoavaliação metacognitiva e registra insight, se houver
            insight = self.digimon.autoanalise.autoavaliar()
            if insight:
                texto_insight = f"Insight: {insight.get('acao_sugerida')} - {insight.get('detalhes', '')}"
                registrar_diario(texto_insight, insight.get('acao_sugerida'), afeto_atual, origem="metacognicao")

            # Se estiver adormecido, sonha e registra sonho
            if hasattr(self.digimon.camadas, "estado_atual") and self.digimon.camadas.estado_atual == "dormant":
                sonho = self.digimon.inconsciente.sonhar()
                msg = sonho.get("mensagem", "")
                registrar_diario(msg, "sonho", afeto_atual, origem="sonho")
                print(f"🌙 Sonho registrado: {msg}")

            # Pequena pausa simulando passagem do tempo
            time.sleep(self.pausa)

        print("✅ Scripturemon concluiu o ciclo simbiótico.")


if __name__ == "__main__":
    loop = ScripturemonLoop(ciclos=5, pausa=2)
    loop.executar()