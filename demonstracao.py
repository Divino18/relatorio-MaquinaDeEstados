from maquina import MaquinaLogin, TransicaoInvalida

m = MaquinaLogin()
for acao in (m.senha_incorreta, m.senha_incorreta, m.senha_incorreta,
             m.senha_correta, m.desbloquear, m.senha_correta):
    try:
        print(f"{acao.__name__:16} -> {acao().name}")
    except TransicaoInvalida as e:
        print(f"{acao.__name__:16} -> ERRO: {e}")

print("Trilha:", m.trilha)