"""Testes para o módulo ``memoria_semantica``."""

import pathlib
import sys

import pytest

# Garante que o repositório esteja no ``sys.path`` para importações relativas.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from digimapas.templo_inicial.scripturemon.memoria_semantica import MemoriaSemantica


@pytest.fixture
def memoria(tmp_path):
    """Retorna instância de ``MemoriaSemantica`` utilizando diretório temporário."""
    return MemoriaSemantica(persist_dir=tmp_path)


def test_registrar_nota_armazena_texto(memoria):
    """Garantir que ``registrar_nota`` salva corretamente o conteúdo da nota."""
    nid = memoria.registrar_nota("texto exemplo", tags=["exemplo"])
    assert memoria.notas[nid].conteudo == "texto exemplo"


def test_buscar_por_tag_retorna_lista(memoria):
    """``buscar_por_tag`` deve retornar lista com notas correspondentes."""
    memoria.registrar_nota("algo", tags=["x"])
    resultado = memoria.buscar_por_tag("x")
    assert isinstance(resultado, list)
    assert len(resultado) == 1


def test_buscar_por_tag_sem_resultados(memoria):
    """Quando a tag não existe, deve retornar lista vazia."""
    assert memoria.buscar_por_tag("inexistente") == []
