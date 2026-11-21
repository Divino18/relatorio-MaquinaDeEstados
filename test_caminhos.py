"""Cobertura de CAMINHOS independentes (C1 a C4).

Cada caminho é executado do estado inicial ao final e confrontado com a
sequência de estados e a trilha de transições da seção 2.7.
"""

import pytest

from maquina import TRANSICOES, Estado, MaquinaLogin

A, U, D, B, OK = (
    Estado.AGUARDANDO,
    Estado.UMA_FALHA,
    Estado.DUAS_FALHAS,
    Estado.BLOQUEADO,
    Estado.AUTENTICADO,
)


def _executar(*passos: str) -> MaquinaLogin:
    m = MaquinaLogin()
    for passo in passos:
        getattr(m, passo)()
    return m


def test_C1_login_na_primeira_tentativa():
    m = _executar("senha_correta")
    assert m.historico == [A, OK]
    assert m.trilha == ["T1"]
    assert m.finalizada


def test_C2_acerta_na_segunda_tentativa():
    m = _executar("senha_incorreta", "senha_correta")
    assert m.historico == [A, U, OK]
    assert m.trilha == ["T2", "T3"]
    assert m.finalizada


def test_C3_acerta_na_terceira_tentativa():
    m = _executar("senha_incorreta", "senha_incorreta", "senha_correta")
    assert m.historico == [A, U, D, OK]
    assert m.trilha == ["T2", "T4", "T5"]
    assert m.finalizada


def test_C4_bloqueio_desbloqueio_e_login():
    m = _executar(
        "senha_incorreta", "senha_incorreta", "senha_incorreta",
        "desbloquear",
        "senha_correta",
    )
    assert m.historico == [A, U, D, B, A, OK]
    assert m.trilha == ["T2", "T4", "T6", "T7", "T1"]
    assert m.finalizada


def test_desbloqueio_zera_o_contador_de_falhas():
    """Após desbloquear, são necessárias 3 novas falhas para bloquear."""
    m = _executar(
        "senha_incorreta", "senha_incorreta", "senha_incorreta",
        "desbloquear",
        "senha_incorreta", "senha_incorreta",
    )
    assert m.estado == D  # e não BLOQUEADO
    m.senha_incorreta()
    assert m.estado == B


# --- Conferência dos números da seção 2.6 e 2.7 ---------------------------

TRILHAS_BASE = {
    "C1": ["T1"],
    "C2": ["T2", "T3"],
    "C3": ["T2", "T4", "T5"],
    "C4": ["T2", "T4", "T6", "T7", "T1"],
}


def test_complexidade_ciclomatica_igual_ao_numero_de_caminhos():
    arestas = len(TRANSICOES)
    nos = len(Estado)
    v_g = arestas - nos + 2

    decisoes = len({t.origem for t in TRANSICOES
                    if sum(u.origem == t.origem for u in TRANSICOES) == 2})

    assert v_g == 4
    assert decisoes + 1 == 4
    assert len(TRILHAS_BASE) == v_g


def test_caminhos_base_cobrem_todas_as_transicoes():
    cobertas = {t for trilha in TRILHAS_BASE.values() for t in trilha}
    assert cobertas == {t.id for t in TRANSICOES}


@pytest.mark.parametrize("nome", list(TRILHAS_BASE))
def test_cada_caminho_introduz_transicao_inedita(nome):
    """Independência linear: cada caminho traz ao menos uma aresta nova
    em relação aos anteriores."""
    nomes = list(TRILHAS_BASE)
    anteriores = {t for n in nomes[: nomes.index(nome)]
                  for t in TRILHAS_BASE[n]}
    assert set(TRILHAS_BASE[nome]) - anteriores
