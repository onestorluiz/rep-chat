import os
import json
from datetime import datetime


def registrar_diario(pensamento, prioridade, afeto, origem="manual"):
    """
    Registra uma entrada no diário reflexivo com timestamp, origem, pensamento, prioridade e afeto.
    """
    dir_path = os.path.dirname(__file__)
    diario_path = os.path.join(dir_path, "diario_reflexivo.md")
    timestamp = datetime.now().isoformat()
    entrada = (
        f"{timestamp}\n"
        f"Origem: {origem}\n"
        f"Pensamento: {pensamento}\n"
        f"Prioridade: {prioridade}\n"
        f"Afeto: {afeto}\n\n"
    )
    with open(diario_path, "a", encoding="utf-8") as diario:
        diario.write(entrada)


def registrar_memoria(pensamento, prioridade, afeto):
    """
    Atualiza ou cria o arquivo de memória imediata com os últimos dados simbóticos.
    Além de atualizar a memória imediata, tenta registrar o pensamento na memória
    semântica agêntica (A-MEM), se o módulo estiver disponível.
    """
    dir_path = os.path.dirname(__file__)
    memoria_path = os.path.join(dir_path, "memoria_imediata.json")
    memoria = {
        "pensamento": pensamento,
        "prioridade": prioridade,
        "afeto": afeto,
        "timestamp": datetime.now().isoformat(),
    }
    with open(memoria_path, "w", encoding="utf-8") as mem_file:
        json.dump(memoria, mem_file, ensure_ascii=False, indent=2)

    # Tenta registrar na memória semântica (A-MEM)
    MemoriaSemantica = None
    try:
        from .memoria_semantica import MemoriaSemantica  # type: ignore
    except Exception:
        try:
            from memoria_semantica import MemoriaSemantica  # type: ignore
        except Exception:
            MemoriaSemantica = None  # type: ignore

    if MemoriaSemantica:
        try:
            ms = MemoriaSemantica()
            # Assegura que prioridade seja uma lista de tags
            if isinstance(prioridade, list):
                tags = [str(tag) for tag in prioridade]
            else:
                tags = [str(prioridade)]
            ms.registrar_nota(conteudo=str(pensamento), tags=tags)
        except Exception as e:
            # Loga o erro silenciosamente para não interromper fluxo principal
            print(f"Erro ao registrar nota na memória semântica: {e}")


def salvar_estado(digimon):
    """
    Salva o estado simbolico do Scripturemon em estado_scripturemon.json.
    """
    dir_path = os.path.dirname(__file__)
    estado_path = os.path.join(dir_path, "estado_scripturemon.json")
    # Recupera valores de afeto e entropia de forma segura
    afeto = None
    if hasattr(digimon, "afeto"):
        valor = getattr(digimon.afeto, "valor", None)
        afeto = valor
    entropia = None
    if hasattr(digimon, "fisica_digital") and hasattr(digimon.fisica_digital, "entropia"):
        entropia = digimon.fisica_digital.entropia
    estado_consciencia = None
    if hasattr(digimon, "camadas"):
        try:
            estado_consciencia = digimon.camadas.estado()
        except Exception:
            estado_consciencia = getattr(digimon.camadas, "estado_atual", None)
    ultima_reflexao = None
    if hasattr(digimon, "analise") and hasattr(digimon.analise, "ultimo_pensamento"):
        ultima_reflexao = digimon.analise.ultimo_pensamento
    estado = {
        "afeto": afeto,
        "entropia": entropia,
        "estado_consciencia": estado_consciencia,
        "ultima_reflexao": ultima_reflexao,
    }
    with open(estado_path, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
