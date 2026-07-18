from datetime import datetime

from lib.cores import cores
from lib.dados import cadastrar_item, registrar_entrada
from lib.msgs import msg_sucesso
from lib.uteis import gerar_id, validar_nome_item, validar_opcao, validar_numeros_inteiros, validar_valor, buscar_id


def titulo_app(txt):
    texto = f'<< {txt.upper()} >>'
    print(f'{cores["cz"]}~{cores["limpa"]}' * 100)
    print(f'{cores["am"]}{texto.center(100)}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 100)

def titulo(txt):
    print(f'{cores["ro"]}{txt.center(100).upper()}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 100)

def separador():
    print(f'{cores["cz"]}~{cores["limpa"]}' * 100)

def menu_principal():
    titulo('Menu Principal')
    opcoes_menu = [
        'Cadastrar item', # 1
        'Registrar entrada de estoque', # 2
        'Registrar saída (requisição)', # 3
        'Listar itens (com quantidade atual e status)', # 4
        'Histórico de movimentação de um item', # 5
        'Itens com estoque abaixo do mínimo', # 6
        'Relatório de consumo por setor', # 7
        'Sair', # 8
    ]
    for item, opcao in enumerate(opcoes_menu):
        print(f'{cores["negrito"]}{cores["az"]}[ {item + 1} ]{cores["limpa"]} {opcao}')
    separador()

def menu(opcoes, txt):
    titulo(txt)
    for item, opcao in enumerate(opcoes):
        print(f'{cores["negrito"]}{cores["az"]}[ {item + 1} ]{cores["limpa"]} {opcao}' , end = '')
        print()
    separador()

def interface_cadastrar_item(nome_arquivo):
    item_id = gerar_id()
    item_nome = validar_nome_item('Digite o nome do item: ')
    unidades_de_medida = ['PC', 'KG', 'LT', 'MT', 'CX']
    menu(unidades_de_medida, 'Selecione a unidade de medida')
    opcao =  validar_opcao(5)
    item_un_med = unidades_de_medida[opcao - 1]
    msg_sucesso(f'Unidade de medida escolhida: {item_un_med}')
    estoque_minimo = validar_numeros_inteiros(f'Digite o estoque minimo do "{item_nome}": ')
    item_preco = validar_valor(f'Digite o valor para cada {item_un_med}: ')
    item_data_de_cadastro = datetime.today().strftime('%d/%m/%Y')
    dados_item = {
        'id': item_id,
        'nome': item_nome,
        'un_med': item_un_med,
        'estoque_minimo': estoque_minimo,
        'preco': item_preco,
        'data_de_cadastro': item_data_de_cadastro
    }
    cadastrar_item(nome_arquivo, dados_item)
    separador()
    msg_sucesso(f'Item {dados_item["nome"]} cadastrado! ID {dados_item["id"]}')
    separador()

def interface_registrar_entrada(arquivo_itens, arquivo_movimentacoes):
    id_registro = gerar_id()
    item_id = buscar_id(arquivo_itens, 'Digite o ID do item: ')
    tipo = 'ENTRADA'
    quantidade = validar_numeros_inteiros(f'Digite a quantidade recebida: ')
    data_entrada = datetime.today().strftime('%d/%m/%Y')
    dados_registro = {
        'id': id_registro,
        'item_id': item_id,
        'tipo': tipo,
        'quantidade': quantidade,
        'data_entrada': data_entrada,
    }
    registrar_entrada(arquivo_movimentacoes, dados_registro)
    separador()
    msg_sucesso(f'Registro {dados_registro["id"]} finalizado!')
    separador()