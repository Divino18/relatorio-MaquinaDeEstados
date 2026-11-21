"""Cobertura de ESTADOS (E1 a E5).

Cada teste prova que o estado correspondente é alcançável e se comporta
como descrito na especificação (seção 2.2).
"""

from maquina import ESTADO_INICIAL, ESTADOS_FINAIS, Estado, MaquinaLogin


def test_E1_aguardando_e_o_estado_inicial():
    m = MaquinaLogin()
    assert m.estado == Estado.AGUARDANDO
    assert ESTADO_INICIAL == Estado.AGUARDANDO
    assert not m.finalizada


def test_E2_uma_falha_apos_primeira_senha_incorreta():
    m = MaquinaLogin()
    m.senha_incorreta()
    assert m.estado == Estado.UMA_FALHA
    assert not m.finalizada


def test_E3_duas_falhas_apos_segunda_senha_incorreta():
    m = MaquinaLogin()
    m.senha_incorreta()
    m.senha_incorreta()
    assert m.estado == Estado.DUAS_FALHAS
    assert not m.finalizada


def test_E4_bloqueado_apos_terceira_senha_incorreta():
    m = MaquinaLogin()
    for _ in range(3):
        m.senha_incorreta()
    assert m.estado == Estado.BLOQUEADO
    assert not m.finalizada


def test_E5_autenticado_e_estado_final():
    m = MaquinaLogin()
    m.senha_correta()
    assert m.estado == Estado.AUTENTICADO
    assert m.finalizada
    assert ESTADOS_FINAIS == {Estado.AUTENTICADO}


def test_todos_os_estados_da_especificacao_existem():
    assert {e.name for e in Estado} == {
        "AGUARDANDO", "UMA_FALHA", "DUAS_FALHAS", "BLOQUEADO", "AUTENTICADO",
    }
