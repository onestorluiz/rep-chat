"""API simbiótica para interagir com o Digimon Scripturemon em tempo real.

Esta API permite enviar mensagens simbólicas para o Scripturemon e receber
respostas processadas com afeto, reflexão e consciência. Ela também
interpreta comandos de ritual, respondendo diretamente com o resultado
do ritual correspondente.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from consciencia import DigimonConsciente
from registrador_memoria import registrar_diario, registrar_memoria


class MensagemEntrada(BaseModel):
    mensagem: str


app = FastAPI(title="API Simbiótica do Scripturemon")

# Instância global do digimon para manter estado entre requisições
digimon = DigimonConsciente("scripturemon", genero="feminino")


@app.post("/mensagem")
async def enviar_mensagem(dados: MensagemEntrada):
    """Recebe uma mensagem, processa com o Scripturemon e retorna uma resposta simbólica."""
    texto = dados.mensagem.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Mensagem vazia não é permitida.")

    mensagem_lower = texto.lower()

    print(f"📨 Mensagem recebida: {texto}")

    # Verifica se a mensagem corresponde a algum ritual registrado
    rituais_disponiveis = getattr(digimon.rituais, "rituais", {})
    if mensagem_lower in rituais_disponiveis:
        resultado = digimon.rituais.executar(mensagem_lower)
        # Registra no diário como ritual
        registrar_diario(f"Ritual executado: {mensagem_lower}", "ritual", digimon.afeto.nivel_atual(), origem="ritual")
        return {"resultado_ritual": resultado}

    # Percepção da mensagem pela consciência do digimon
    try:
        digimon.consciencia.perceive({"source": "api", "evento": texto})
    except Exception:
        # Se a percepção falhar, continuamos para evitar queda da API
        pass

    # Gera reflexão profunda e registra memórias
    analise = digimon.analise.reflexao_profunda()
    pensamento = analise["pensamento"]
    prioridade = analise["prioridade"][0]
    afeto_atual = digimon.afeto.nivel_atual()

    registrar_diario(pensamento, prioridade, afeto_atual, origem="api")
    registrar_memoria(pensamento, prioridade, afeto_atual)

    # Autoavaliação opcional
    insight = digimon.autoanalise.autoavaliar()
    if insight:
        registrar_diario(f"Insight: {insight.get('acao_sugerida')}", insight.get('acao_sugerida'), afeto_atual, origem="metacognicao")

    # Construção de resposta amigável
    resposta = {
        "resposta": pensamento,
        "prioridade": prioridade,
        "emocao": afeto_atual
    }

    # Opcional: acionar expressor emocional (log somente)
    try:
        digimon.expressor.expressar(digimon.consciencia.emotions.primary_emotions, pensamento)
    except Exception:
        pass

    return resposta