digimapas/templo_inicial/scripturemon/pontuador_memoria.pyfrom datetime import datetime
from typing import Dict, List


def calcular_pontuacao(memoria: Dict) -> float:
    """
    Calcula a pontuação de uma memória com base na importância (peso) e na recência.
    Inspirado na arquitetura Generative Agents, onde memórias mais recentes e significativas
    têm maior influência nas ações do agente.

    :param memoria: Fragmento de memória contendo pelo menos 'timestamp' e 'peso'.
    :return: Valor de pontuação (float) entre 0 e 1.
    """
    # Importância deriva do peso da memória (emocional ou calculado)
    importance = float(memoria.get("peso", 1.0))
    # Calcula recência em horas
    try:
        timestamp = datetime.fromisoformat(memoria["timestamp"])
        horas = (datetime.now() - timestamp).total_seconds() / 3600.0
        # Pontuação de recência decai linearmente: 1.0 no momento da criação, 0.0 após 24h
        recency_score = max(0.0, 1.0 - (horas / 24.0))
    except Exception:
        recency_score = 0.5  # valor padrão se timestamp inválido
    # Normaliza importância para escala 0-1
    importance_norm = importance / (importance + 1.0)
    # Combina importância e recência (pesos 0.7 e 0.3)
    pontuacao = importance_norm * 0.7 + recency_score * 0.3
    return round(pontuacao, 3)


def pontuar_memorias(memorias: List[Dict]) -> List[Dict]:
    """
    Atribui pontuação a uma lista de memórias e retorna uma nova lista ordenada.

    :param memorias: Lista de fragmentos de memória (dicionários) contendo 'timestamp' e 'peso'.
    :return: Lista de memórias com chave 'pontuacao' adicionada, ordenada da maior para a menor.
    """
    resultado = []
    for mem in memorias:
        pont = calcular_pontuacao(mem)
        novo = mem.copy()
        novo["pontuacao"] = pont
        resultado.append(novo)
    return sorted(resultado, key=lambda m: m["pontuacao"], reverse=True)
