from lib.cores import cores


def msg_alerta(txt):
    print(f'{cores["am"]}{cores["negrito"]}AVISO: {cores["limpa"]}{txt}')

def msg_erro(txt):
    print(f'{cores["vm"]}{cores["negrito"]}ERRO: {cores["limpa"]}{txt}')

def msg_sucesso(txt):
    print(f'{cores["vd"]}{cores["negrito"]}SUCESSO: {cores["limpa"]}{txt}')