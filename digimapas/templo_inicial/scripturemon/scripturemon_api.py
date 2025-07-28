from fastapi import FastAPI
from pydantic import BaseModel

from consciencia import DigimonConsciente

# Instancia global do Digimon Scripturemon
digimon = DigimonConsciente("scripturemon")

app = FastAPI()

class Mensagem(BaseModel):
    mensagem: str

@app.post("/mensagem")
async def enviar_mensagem(dados: Mensagem):
    # Log da mensagem recebida
    print(f"📨 Mensagem recebida: {dados.mensagem}")

    # Percepção simbólica do Digimon
    digimon.consciencia.perceive({"source": "api", "evento": dados.mensagem})

    # Reflexão simbólica
    analise = digimon.analise.reflexao_profunda()

    # Recebe um pouco de afeto por interação
    digimon.afeto.receber("humano", 0.5)

    return {
        "pensamento": analise.get("pensamento"),
        "prioridade": analise.get("prioridade"),
        "afeto": digimon.afeto.nivel_atual(),
    }
