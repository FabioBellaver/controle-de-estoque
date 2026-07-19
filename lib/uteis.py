from nanoid import generate

from lib.arquivos import ler_arquivo_itens
from lib.dados import dados_estoque
from lib.msgs import msg_erro, msg_sucesso


def validar_opcao(maximo=0):
    while True:
        try:
            opcao = int(input('Escolha uma opção >> '))
            if opcao <= 0:
                msg_erro('Digite um número inteiro válido.')
                continue
            elif opcao > maximo:
                msg_erro('Opção inválida.')
                continue
            return opcao
        except ValueError:
            msg_erro('Digite um número inteiro válido (apenas números).')


def gerar_id():
    alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    id_transacao = generate(alfabeto, 8)
    return id_transacao


def validar_nome_item(txt):
    while True:
        nome_item = str(input(txt)).strip().title()
        if nome_item == '':
            msg_erro('Nome inválido.')
        elif len(nome_item) > 35:
            msg_erro('O nome deve conter no máximo 35 caracteres.')
        elif nome_item.isnumeric():
            msg_erro('O nome não deve conter apenas números.')
        else:
            return nome_item.upper()


def validar_numeros_inteiros(msg):
    while True:
        try:
            valor = int(input(msg))
            if valor < 0:
                msg_erro(f'Valor inválido.')
            return valor
        except ValueError:
            msg_erro('Digite um número inteiro válido (apenas números).')


def validar_valor(msg):
    while True:
        entrada_valor = input(msg).strip().replace(',', '.')
        try:
            valor = float(entrada_valor)
            if valor <= 0:
                msg_erro('O valor da transação deve ser maior que zero.')
            else:
                return valor
        except ValueError:
            msg_erro('Digite um valor numérico válido.')


def buscar_id(nome_arquivo, msg):
    itens = ler_arquivo_itens(nome_arquivo)
    while True:
        id_encontrado = False
        entrada_id = input(msg).strip().upper()
        if entrada_id == '':
            msg_erro('ID inválido.')
        elif len(entrada_id) > 8 or len(entrada_id) < 8:
            msg_erro('IDs tem 8 caracteres apenas.')
        else:
            for item in itens:
                if item["id"] == entrada_id:
                    msg_sucesso(f'ID "{item["id"]}" encontrado.')
                    id_encontrado = True
                    return entrada_id
        if not id_encontrado:
            msg_erro(f'ID {entrada_id} não foi encontrado.')


def formatar_para_real(valor):
    valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor_formatado


def buscar_qtd_estoque_id(arquivo_itens, arquivo_movimentacoes, id_item):
    estoque = dados_estoque(arquivo_itens, arquivo_movimentacoes)
    quantidade_estoque_item = 0
    nome_item = ''
    for item in estoque:
        if item["id_item"] == id_item:
            quantidade_estoque_item = item["quantidade"]
            nome_item = item["nome"]
            break
    return [quantidade_estoque_item, nome_item]
