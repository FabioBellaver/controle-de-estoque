from datetime import datetime

from lib.arquivos import ler_arquivo_itens
from lib.cores import cores
from lib.dados import cadastrar_item, registrar_entrada, registrar_saida, dados_estoque
from lib.msgs import msg_sucesso, msg_alerta
from lib.uteis import gerar_id, validar_nome_item, validar_opcao, validar_numeros_inteiros, validar_valor, buscar_id, \
    formatar_para_real

def titulo_app(txt):
    texto = f'<< {txt.upper()} >>'
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)
    print(f'{cores["am"]}{texto.center(130)}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)

def titulo(txt):
    print(f'{cores["am"]}{txt.center(140).upper()}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)

def separador():
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)

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
    itens = ler_arquivo_itens(arquivo_itens)
    if itens:
        id_registro = gerar_id()
        item_id = buscar_id(arquivo_itens, 'Digite o ID do item: ')
        tipo = 'ENTRADA'
        quantidade = validar_numeros_inteiros(f'Digite a quantidade recebida: ')
        data_entrada = datetime.today().strftime('%d/%m/%Y')
        dados_entrada = {
            'id': id_registro,
            'item_id': item_id,
            'tipo': tipo,
            'quantidade': quantidade,
            'data_entrada': data_entrada,
        }
        registrar_entrada(arquivo_movimentacoes, dados_entrada)
        separador()
        msg_sucesso(f'Registro ID "{dados_entrada["id"]}" finalizado!')
        separador()
    else:
        msg_alerta('Não existem itens cadastrados. Não é possível registrar uma entrada.')

def interface_registrar_saida(arquivo_itens, arquivo_movimentacoes = ''):
    itens = ler_arquivo_itens(arquivo_itens)
    if itens:
        id_registro = gerar_id()
        item_id = buscar_id(arquivo_itens, 'Digite o ID do item: ')
        tipo = 'SAIDA'
        quantidade = validar_numeros_inteiros(f'Digite a quantidade entregue: ')
        setores = ['RECURSOS HUMANOS', 'FINANCEIRO', 'JURIDICO', 'LOGISTICA', 'RECEPCAO', 'SUPORTE TECNICO']
        menu(setores, 'Selecione o setor requisitante')
        opcao = validar_opcao(6)
        setor_requisitante = setores[opcao - 1]
        data_saida = datetime.today().strftime('%d/%m/%Y')
        dados_saida = {
            'id': id_registro,
            'item_id': item_id,
            'tipo': tipo,
            'quantidade': quantidade,
            'setor_requisitante': setor_requisitante,
            'data_saida': data_saida
        }
        registrar_saida(arquivo_movimentacoes, dados_saida)
        separador()
        msg_sucesso(f'Registro ID "{dados_saida["id"]}" finalizado!')
        separador()
    else:
        msg_alerta('Não existem itens cadastrados. Não é possível registrar uma entrada.')

def cabecalho_relatorio_estoque():
    #cabecalho_tabela(['ID', 'Produto', 'Un', 'Quantidade', 'Preço UN', 'Valor Total', 'Min. Estoque', 'Status'])
    print(f'{cores["negrito"]}{cores["cz"]}'
          f'{"ID":<10}'
          f'{"PRODUTO":<50}'
          f'{"UMB":<10}'
          f'{"QTD":<10}'
          f'{"EST.MIN.":<10}'
          f'{"PREÇO UN.":<15}'
          f'{"VALOR TOTAL":<15}'
          f'{"STATUS":<10}'
          f'{cores["limpa"]}')
    separador()

def interface_relatorio_estoque(arquivo_itens, arquivo_movimentacoes):
    relatorio = dados_estoque(arquivo_itens, arquivo_movimentacoes)
    relatorio.sort(key=lambda item: item['nome'])
    qtd_itens = len(relatorio)
    valor_estoque_total = 0
    cabecalho_relatorio_estoque()
    for item in relatorio:
        if item["valor_total"]:
            valor_estoque_total += item["valor_total"]
        print(f'{item["id_item"]:<10}'
              f'{item["nome"]:<50}'
              f'{item["un_med"]:<10}'
              f'{item["quantidade"]:<10}'
              f'{item["estoque_minimo"]:<10}'
              f'{formatar_para_real(item["preco_un"]):<15}'
              f'{formatar_para_real(item["valor_total"]):<15}', end='')
        if item['status'] == 'OK':
            print(f'{cores["vd"]}{item["status"]:<10}{cores["limpa"]}')
        elif item['status'] == 'REPOSIÇÃO':
            print(f'{cores["vm"]}{item["status"]:<10}{cores["limpa"]}')
        elif item['status'] == 'ATENÇÃO':
            print(f'{cores["am"]}{item["status"]:<10}{cores["limpa"]}')
        elif item['status'] == 'SEM ESTOQUE':
            print(f'{cores["vm"]}{item["status"]:<10}{cores["limpa"]}')
    separador()
    txt = f'{cores["negrito"]}Quantidade de itens: {cores["limpa"]}{qtd_itens} | {cores["negrito"]}Valor total estoque:{cores["limpa"]} {formatar_para_real(valor_estoque_total)}'
    print(txt.center(130))
    separador()