"""Cobertura de TRANSIÇÕES (T1 a T7) e rejeição das 8 inválidas.

Os casos são parametrizados a partir da especificação (seção 2.4).
Cada transição parte de um estado alcançado por eventos válidos.
"""

import itertools

import pytest

from maquina import TRANSICOES, Estado, Evento, TransicaoInvalida

# (id, origem, evento, destino) escritos à mão, independentes do código,
# para que o teste confronte a implementação com a especificação.
ESPECIFICACAO = [
    ("T1", Estado.AGUARDANDO, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    ("T2", Estado.AGUARDANDO, Evento.SENHA_INCORRETA, Estado.UMA_FALHA),
    ("T3", Estado.UMA_FALHA, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    ("T4", Estado.UMA_FALHA, Evento.SENHA_INCORRETA, Estado.DUAS_FALHAS),
    ("T5", Estado.DUAS_FALHAS, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    ("T6", Estado.DUAS_FALHAS, Evento.SENHA_INCORRETA, Estado.BLOQUEADO),
    ("T7", Estado.BLOQUEADO, Evento.DESBLOQUEAR, Estado.AGUARDANDO),
]

INVALIDAS = [
    (Estado.AGUARDANDO, Evento.DESBLOQUEAR),
    (Estado.UMA_FALHA, Evento.DESBLOQUEAR),
    (Estado.DUAS_FALHAS, Evento.DESBLOQUEAR),
    (Estado.BLOQUEADO, Evento.SENHA_CORRETA),
    (Estado.BLOQUEADO, Evento.SENHA_INCORRETA),
    (Estado.AUTENTICADO, Evento.SENHA_CORRETA),
    (Estado.AUTENTICADO, Evento.SENHA_INCORRETA),
    (Estado.AUTENTICADO, Evento.DESBLOQUEAR),
]


@pytest.mark.parametrize(
    "id_, origem, evento, destino",
    ESPECIFICACAO,
    ids=[t[0] for t in ESPECIFICACAO],
)
def test_transicao_valida(maquina_em, id_, origem, evento, destino):
    m = maquina_em(origem)
    trilha_antes = list(m.trilha)

    novo = m.processar(evento)

    assert novo == destino
    assert m.estado == destino
    assert m.trilha == trilha_antes + [id_]


def test_tabela_implementada_igual_a_especificacao():
    implementada = [(t.id, t.origem, t.evento, t.destino) for t in TRANSICOES]
    assert implementada == ESPECIFICACAO


@pytest.mark.parametrize(
    "origem, evento",
    INVALIDAS,
    ids=[f"{o.name}-{e.value}" for o, e in INVALIDAS],
)
def test_invalida_e_rejeitada_sem_alterar_estado(maquina_em, origem, evento):
    m = maquina_em(origem)
    estado_antes = m.estado
    trilha_antes = list(m.trilha)
    historico_antes = list(m.historico)

    with pytest.raises(TransicaoInvalida) as exc:
        m.processar(evento)

    assert exc.value.estado == origem
    assert exc.value.evento == evento
    assert m.estado == estado_antes
    assert m.trilha == trilha_antes
    assert m.historico == historico_antes


def test_validas_e_invalidas_particionam_as_15_combinacoes():
    todas = set(itertools.product(Estado, Evento))
    validas = {(o, e) for _, o, e, _ in ESPECIFICACAO}
    invalidas = set(INVALIDAS)

    assert len(todas) == 15
    assert len(validas) == 7
    assert len(invalidas) == 8
    assert validas.isdisjoint(invalidas)
    assert validas | invalidas == todas
