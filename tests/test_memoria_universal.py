"""Testes para o módulo ``memoria_universal``."""

import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from digimapas.templo_inicial.scripturemon.memoria_universal import MemoriaUniversal


@pytest.fixture
def memoria_universal():
    """Instancia ``MemoriaUniversal`` desligando integração com memória semântica."""
    mu = MemoriaUniversal("teste")
    mu.semantica_cls = None
    return mu


def test_extrair_e_atualizar_retorna_lista(memoria_universal):
    """Chamada deve retornar lista de candidatos analisados."""
    resultado = memoria_universal.extrair_e_atualizar("evento", "pensamento")
    assert isinstance(resultado, list)
    assert "evento" in resultado


def test_extrair_e_atualizar_sem_texto(memoria_universal):
    """Sem entrada válida, retorna lista vazia."""
    assert memoria_universal.extrair_e_atualizar("", "") == []
