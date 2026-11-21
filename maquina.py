"""Máquina de estados: login com bloqueio por tentativas.

Implementa a especificação do relatório:
  - Estados E1..E5
  - Eventos: senha_correta, senha_incorreta, desbloquear
  - Transições T1..T7 (as demais combinações são inválidas)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Estado(Enum):
    AGUARDANDO = "AGUARDANDO"      # E1 (inicial)
    UMA_FALHA = "UMA_FALHA"        # E2
    DUAS_FALHAS = "DUAS_FALHAS"    # E3
    BLOQUEADO = "BLOQUEADO"        # E4
    AUTENTICADO = "AUTENTICADO"    # E5 (final)


class Evento(Enum):
    SENHA_CORRETA = "senha_correta"
    SENHA_INCORRETA = "senha_incorreta"
    DESBLOQUEAR = "desbloquear"


class TransicaoInvalida(Exception):
    """Evento não previsto para o estado atual."""

    def __init__(self, estado: Estado, evento: Evento) -> None:
        self.estado = estado
        self.evento = evento
        super().__init__(
            f"Evento '{evento.value}' inválido no estado '{estado.name}'"
        )


@dataclass(frozen=True)
class Transicao:
    id: str
    origem: Estado
    evento: Evento
    destino: Estado


# Tabela de transições válidas (seção 2.4 da especificação).
TRANSICOES: tuple[Transicao, ...] = (
    Transicao("T1", Estado.AGUARDANDO, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    Transicao("T2", Estado.AGUARDANDO, Evento.SENHA_INCORRETA, Estado.UMA_FALHA),
    Transicao("T3", Estado.UMA_FALHA, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    Transicao("T4", Estado.UMA_FALHA, Evento.SENHA_INCORRETA, Estado.DUAS_FALHAS),
    Transicao("T5", Estado.DUAS_FALHAS, Evento.SENHA_CORRETA, Estado.AUTENTICADO),
    Transicao("T6", Estado.DUAS_FALHAS, Evento.SENHA_INCORRETA, Estado.BLOQUEADO),
    Transicao("T7", Estado.BLOQUEADO, Evento.DESBLOQUEAR, Estado.AGUARDANDO),
)

# Índice (origem, evento) -> Transicao, para consulta O(1).
_INDICE: dict[tuple[Estado, Evento], Transicao] = {
    (t.origem, t.evento): t for t in TRANSICOES
}

ESTADO_INICIAL = Estado.AGUARDANDO
ESTADOS_FINAIS = frozenset({Estado.AUTENTICADO})


class MaquinaLogin:
    """Máquina de estados do processo de login.

    Atributos públicos:
        estado:    estado atual.
        historico: sequência de estados visitados (inclui o inicial).
        trilha:    IDs das transições executadas (ex.: ["T2", "T3"]).
    """

    def __init__(self) -> None:
        self.estado: Estado = ESTADO_INICIAL
        self.historico: list[Estado] = [ESTADO_INICIAL]
        self.trilha: list[str] = []

    @property
    def finalizada(self) -> bool:
        return self.estado in ESTADOS_FINAIS

    def processar(self, evento: Evento) -> Estado:
        """Aplica o evento e devolve o novo estado.

        Levanta TransicaoInvalida (sem alterar o estado) se o evento
        não for permitido no estado atual.
        """
        transicao = _INDICE.get((self.estado, evento))
        if transicao is None:
            raise TransicaoInvalida(self.estado, evento)

        self.estado = transicao.destino
        self.historico.append(self.estado)
        self.trilha.append(transicao.id)
        return self.estado

    # Atalhos de leitura mais natural para o chamador.
    def senha_correta(self) -> Estado:
        return self.processar(Evento.SENHA_CORRETA)

    def senha_incorreta(self) -> Estado:
        return self.processar(Evento.SENHA_INCORRETA)

    def desbloquear(self) -> Estado:
        return self.processar(Evento.DESBLOQUEAR)