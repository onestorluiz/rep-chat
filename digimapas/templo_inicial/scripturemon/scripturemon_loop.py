import os
import time
from datetime import datetime
from consciencia import DigimonConsciente


class ScripturemonLoop:
    def __init__(self):
        """Inicializa o ciclo simbótico de Scripturemon"""
        self.digimon = DigimonConsciente("scripturemon")
        # Carrega o ritual inicial se existir
        manifesto_path = os.path.join("dados_globais", "manifestos", "ritual_inicial.md")
        if os.path.exists(manifesto_path):
            with open(manifesto_path, "r", encoding="utf-8") as f:
                conteudo = f.read()
            print("\U0001f4dc Ritual inicial carregado:")
            print(conteudo)
        else:
            print(f"\u26a0\ufe0f Ritual inicial não encontrado em {manifesto_path}")

    def executar_ciclos(self, ciclos: int = 5):
        """Executa uma série de ciclos vivos para Scripturemon"""
        for ciclo in range(1, ciclos + 1):
            print(f"✨ SCRIPTUREMON INICIANDO CICLO {ciclo}")
            # Executa comportamento principal
            try:
                self.digimon.viver()
            except Exception as e:
                print("⚠️ Erro ao executar viver:", e)
            # Recebe um pouco de afeto do mundo
            try:
                self.digimon.afeto.receber("mundo", 0.5)
            except Exception:
                pass
            # Atualiza camadas de consciência
            try:
                self.digimon.camadas.atualizar_estado(
                    self.digimon.consciencia.awareness_level,
                    self.digimon.consciencia.energy_level,
                    self.digimon.consciencia.consciousness_depth
                )
            except Exception:
                pass
            # Análise interna profunda
            pensamento = None
            emocao = None
            try:
                analise = self.digimon.analise.reflexao_profunda()
                pensamento = analise.get("pensamento")
                # Determina a emoção dominante atual
                emocao = max(self.digimon.consciencia.emotions.primary_emotions.items(), key=lambda x: x[1])[0]
                print(f"\U0001f4ad Pensamento: {pensamento}")
                print(f"🎯 Emoção dominante: {emocao}")
            except Exception as e:
                print("⚠️ Erro na análise interna:", e)
            # Registra no diário reflexivo
            diario_path = os.path.join(os.path.dirname(__file__), "diario_reflexivo.md")
            if pensamento:
                try:
                    with open(diario_path, "a", encoding="utf-8") as df:
                        df.write(f"\n## {datetime.now().isoformat()}\n")
                        df.write(f"Pensamento: {pensamento}\n")
                except Exception as e:
                    print("⚠️ Não foi possível escrever no diário:", e)
            # Pausa simbólica
            time.sleep(2)
        print("✅ Scripturemon concluiu o ciclo simbótico.")


if __name__ == "__main__":
    loop = ScripturemonLoop()
    loop.executar_ciclos()
