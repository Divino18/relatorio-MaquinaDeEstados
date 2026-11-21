# Máquina de Estados — Autenticação com bloqueio por tentativas

Trabalho prático do Grupo 09 (Divino Chaves Stefa, Francisco Nascimento Bendô e
Enzo Medeiros Nóbrega). O relatório em PDF é entregue separadamente; este
repositório contém o código-fonte completo e os testes automatizados.

## O que é
Máquina de estados finitos de login: 5 estados (E1 AGUARDANDO, E2 UMA_FALHA,
E3 DUAS_FALHAS, E4 BLOQUEADO, E5 AUTENTICADO), 3 eventos (senha_correta,
senha_incorreta, desbloquear) e 7 transições (T1 a T7). Complexidade ciclomática
V(G) = E − N + 2 = 7 − 5 + 2 = 4, ou seja, 4 caminhos independentes (C1 a C4).

## Arquivos
| Arquivo | Conteúdo |
|---|---|
| `maquina.py` | Implementação: enums `Estado` e `Evento`, tabela `TRANSICOES` e classe `MaquinaLogin` |
| `conftest.py` | Fixture `maquina_em`, que leva a máquina a qualquer estado |
| `test_estados.py` | Testes de estados (6 casos) |
| `test_transicoes.py` | Testes de transições válidas e inválidas (17 casos) |
| `test_caminhos.py` | Testes dos caminhos independentes C1 a C4 (11 casos) |
| `demonstracao.py` | Execução ilustrativa dos 4 caminhos (opcional) |
| `pytest.ini`, `requirements.txt` | Configuração e dependências |

## Como executar
```bash
pip install -r requirements.txt
pytest                                   # 34 testes, 100% automatizados
pytest --cov=maquina --cov-report=term-missing   # cobertura de código (100%)
python demonstracao.py                   # demonstração dos caminhos
```
Requer Python 3.10 ou superior.
