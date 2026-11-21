"""Fixtures compartilhadas.

`maquina_em` leva a máquina a um estado alvo usando apenas eventos
válidos (sem atribuir `estado` diretamente), garantindo que o estado
de partida dos testes seja realmente alcançável.
"""

import pytest

from maquina import Estado, Evento, MaquinaLogin

# Sequência mínima de eventos que leva do estado inicial a cada estado.
CAMINHO_ATE = {
    Estado.AGUARDANDO: [],
    Estado.UMA_FALHA: [Evento.SENHA_INCORRETA],
    Estado.DUAS_FALHAS: [Evento.SENHA_INCORRETA] * 2,
    Estado.BLOQUEADO: [Evento.SENHA_INCORRETA] * 3,
    Estado.AUTENTICADO: [Evento.SENHA_CORRETA],
}


@pytest.fixture
def maquina_em():
    """Fábrica: maquina_em(Estado.X) devolve uma máquina já em X."""

    def _criar(estado: Estado) -> MaquinaLogin:
        m = MaquinaLogin()
        for evento in CAMINHO_ATE[estado]:
            m.processar(evento)
        assert m.estado == estado  # pré-condição do teste
        return m

    return _criar
