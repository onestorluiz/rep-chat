"""
Modulo de reflexao de alto nivel para Scripturemon.

Este modulo fornece funcoes para analisar as memorias semanticas registradas
(A‑MEM) e gerar resumos de alto nivel. A ideia eh utilizar as tags e o conteudo
para identificar temas recorrentes, calcular frequencia de tags e compor
resumos baseados nos fragmentos de memoria mais relevantes. Ele foi
inspirado por tecnicas de “Generative Agents” para reflexao.

Functions:
    gerar_relatorio_tags(memorias): Retorna um dicionario com a frequencia de cada tag.
    resumir_por_tags(memorias, top_n): Gera resumos concatenando conteudos das memórias
        por tag, apenas para as top_n tags mais frequentes.
    resumir_memorias_semanticas(memoria_semantica, top_n): Carrega notas da memoria
        semantica e retorna os resumos das tags.
"""

from collections import Counter
from typing import Dict, List, Any


def gerar_relatorio_tags(memorias: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calcula a frequencia de cada tag nas memorias fornecidas.

    Args:
        memorias: Lista de memorias semanticas, cada uma contendo um campo 'tags'.

    Returns:
        Dicionario onde a chave e a tag e o valor e o numero de ocorrencias.
    """
    contador: Counter[str] = Counter()
    for memoria in memorias:
        tags = memoria.get("tags", [])
        if tags:
            contador.update(tags)
    return dict(contador)


def resumir_por_tags(memorias: List[Dict[str, Any]], top_n: int = 5) -> Dict[str, str]:
    """Gera resumos simples concatenando fragmentos por tag.

    Este metodo seleciona as top_n tags mais frequentes e concatena os
    conteudos das memorias correspondentes em um unico texto por tag.

    Args:
        memorias: Lista de memorias semanticas com campos 'conteudo' e 'tags'.
        top_n: Numero de tags mais frequentes a considerar.

    Returns:
        Dicionario mapeando cada tag para um resumo (string).
    """
    relatorio = gerar_relatorio_tags(memorias)
    # Ordena as tags por frequencia decrescente
    top_tags = [tag for tag, _ in sorted(relatorio.items(), key=lambda item: item[1], reverse=True)[:top_n]]
    resumos: Dict[str, str] = {}
    for tag in top_tags:
        fragmentos = [memoria.get("conteudo", "") for memoria in memorias if tag in memoria.get("tags", [])]
        # Concatena os fragmentos com espaco
        resumo = " ".join(fragmentos)
        resumos[tag] = resumo.strip()
    return resumos


def resumir_memorias_semanticas(memoria_semantica: Any, top_n: int = 5) -> Dict[str, str]:
    """Carrega notas da memoria semantica e retorna resumos por tag.

    Este funcao e um utilitario que integra a classe MemoriaSemantica definida
    no modulo memoria_semantica. Ele invoca o metodo carregar_notas() para
    recuperar todas as notas existentes e gera resumos para as tags mais
    frequentes.

    Args:
        memoria_semantica: Instancia de MemoriaSemantica.
        top_n: Numero de tags a considerar.

    Returns:
        Dicionario mapeando tags para resumos.
    """
    try:
        notas = memoria_semantica.carregar_notas()
    except Exception:
        notas = []
    return resumir_por_tags(notas, top_n)


if __name__ == "__main__":
    # Exemplo de uso simplificado. Isso nao sera executado quando importado como modulo.
    try:
        from .memoria_semantica import MemoriaSemantica  # tipo: ignore
    except ImportError:
        from memoria_semantica import MemoriaSemantica  # fallback quando executado isolado

    mem_sem = MemoriaSemantica()
    notas = mem_sem.carregar_notas()
    relatorio = resumir_memorias_semanticas(mem_sem, top_n=3)
    for tag, resumo in relatorio.items():
        print(f"Tag: {tag}\nResumo: {resumo}\n")
