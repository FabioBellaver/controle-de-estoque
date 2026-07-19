from datetime import datetime

from lib.arquivos import ler_arquivo_itens
from lib.cores import cores
from lib.dados import cadastrar_item, registrar_entrada, registrar_saida, dados_estoque, dados_movimentacoes
from lib.msgs import msg_sucesso, msg_alerta, msg_erro
from lib.uteis import gerar_id, validar_nome_item, validar_opcao, validar_numeros_inteiros, validar_valor, buscar_id, \
    formatar_para_real, buscar_qtd_estoque_id


def titulo_app(txt):
    texto = f'<< {txt.upper()} >>'
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)
    print(f'{cores["am"]}{texto.center(130)}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)


def titulo(txt):
    print(f'{cores["am"]}{txt.center(130).upper()}{cores["limpa"]}')
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)


def separador():
    print(f'{cores["cz"]}~{cores["limpa"]}' * 130)


def menu_principal():
    titulo('Menu Principal')
    opcoes_menu = [
        'Cadastrar item',  # 1
        'Registrar entrada de estoque',  # 2
        'Registrar saída (requisição)',  # 3
        'Listar itens (com quantidade atual e status)',  # 4
        'Histórico de movimentação de um item',  # 5
        'Itens com estoque abaixo do mínimo',  # 6
        'Relatório de consumo por setor',  # 7
        'Sair',  # 8
    ]
    for item, opcao in enumerate(opcoes_menu):
        print(f'{cores["negrito"]}{cores["az"]}[ {item + 1} ]{cores["limpa"]} {opcao}')
    separador()


def menu(opcoes, txt):
    titulo(txt)
    for item, opcao in enumerate(opcoes):
        print(f'{cores["negrito"]}{cores["az"]}[ {item + 1} ]{cores["limpa"]} {opcao}', end='')
        print()
    separador()


def interface_cadastrar_item(nome_arquivo):
    item_id = gerar_id()
    item_nome = validar_nome_item('Digite o nome do item: ')
    unidades_de_medida = ['PC', 'KG', 'LT', 'MT', 'CX']
    menu(unidades_de_medida, 'Selecione a unidade de medida')
    opcao = validar_opcao(5)
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


def interface_registrar_saida(arquivo_itens, arquivo_movimentacoes=''):
    itens = ler_arquivo_itens(arquivo_itens)
    if itens:
        id_registro = gerar_id()
        item_id = buscar_id(arquivo_itens, 'Digite o ID do item: ')
        tipo = 'SAIDA'
        qtd_estoque_e_nome = buscar_qtd_estoque_id(arquivo_itens, arquivo_movimentacoes, item_id)
        qtd_estoque = qtd_estoque_e_nome[0]
        nome = qtd_estoque_e_nome[1]
        while True:
            quantidade = validar_numeros_inteiros(f'Digite a quantidade entregue: ')
            valido = 0 < quantidade <= qtd_estoque
            if valido:
                break
            elif quantidade > qtd_estoque:
                msg_erro(f'Não é possível registrar saída maior que estoque {nome} atual.| QTD ESTOQUE: {qtd_estoque}')
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
    dados = ler_arquivo_itens(arquivo_itens)
    if dados:
        relatorio = dados_estoque(arquivo_itens, arquivo_movimentacoes)
        relatorio.sort(key=lambda item: item['nome'])
        qtd_itens = len(relatorio)
        itens_sem_estoque = 0
        valor_estoque_total = 0
        cabecalho_relatorio_estoque()
        for item in relatorio:
            if item["valor_total"]:
                valor_estoque_total += item["valor_total"]
            elif item["quantidade"] == 0:
                itens_sem_estoque += 1
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
        resumo = (
            f'{cores["negrito"]}Quantidade de itens cadastrados: {cores["limpa"]}{qtd_itens} | '
            f'{cores["negrito"]}Quantidade de itens disponíveis: {cores["limpa"]}{qtd_itens - itens_sem_estoque} | '
            f'{cores["negrito"]}Valor total estoque:{cores["limpa"]} {formatar_para_real(valor_estoque_total)}'
        )
        print(resumo.center(130))
        separador()
    else:
        msg_alerta('Não existem itens cadastrados.')


def cabecalho_relatorio_movimentacoes():
    print(f'{cores["negrito"]}{cores["cz"]}'
          f'{"ID MOV.":<12}'
          f'{"TIPO":<10}'
          f'{"ID ITEM":<12}'
          f'{"PRODUTO":<40}'
          f'{"UMB":<8}'
          f'{"QTD":<10}'
          f'{"DATA":<15}'
          f'{"SETOR":<20}'
          f'{cores["limpa"]}')
    separador()


def interface_historico_movimentacoes(arquivo_itens, arquivo_movimentacoes):
    dados = ler_arquivo_itens(arquivo_itens)
    if dados:
        item_id = buscar_id(arquivo_itens, 'Digite o ID do item: ')
        relatorio = dados_movimentacoes(arquivo_itens, arquivo_movimentacoes)
        relatorio.sort(key=lambda item: datetime.strptime(item['data'], '%d/%m/%Y'), reverse=True)
        total_mov = 0
        total_entradas = 0
        total_saidas = 0
        qtd_estoque = 0
        cabecalho_relatorio_movimentacoes()
        for movimento in relatorio:
            if movimento['id_item'] == item_id:
                total_mov += 1
                tipo = ''
                quantidade = ''
                if movimento['tipo'] == 'ENTRADA':
                    total_entradas += 1
                    qtd_estoque += movimento['quantidade']
                    txt_tipo = f'{movimento["tipo"]:<10}'
                    tipo = f'{cores["vd"]}{txt_tipo}{cores["limpa"]}'
                    txt_qtd = f'{movimento["quantidade"]:<10}'
                    quantidade = f'{cores["vd"]}{txt_qtd}{cores["limpa"]}'
                elif movimento['tipo'] == 'SAIDA':
                    total_saidas += 1
                    qtd_estoque -= movimento['quantidade']
                    txt_tipo = f'{movimento["tipo"]:<10}'
                    tipo = f'{cores["vm"]}{txt_tipo}{cores["limpa"]}'
                    txt_qtd = f'-{movimento["quantidade"]:<9}'
                    quantidade = f'{cores["vm"]}{txt_qtd}{cores["limpa"]}'
                print(f'{movimento["id_movimento"]:<12}'
                      f'{tipo}'
                      f'{movimento["id_item"]:<12}'
                      f'{movimento["nome"]:<40}'
                      f'{movimento["un_med"]:<8}'
                      f'{quantidade}'
                      f'{movimento["data"]:<15}'
                      f'{movimento["setor_requisitante"]:<20}')
        separador()
        resumo = (f'{cores["negrito"]}Total de operações: {cores["limpa"]}{total_mov} | '
                  f'{cores["negrito"]}Total de entradas: {cores["limpa"]}{total_entradas} | '
                  f'{cores["negrito"]}Total de saídas: {cores["limpa"]}{total_saidas} | '
                  f'{cores["negrito"]}Saldo atual: {cores["limpa"]}{qtd_estoque}')
        print(resumo.center(130))
        separador()
    else:
        msg_alerta('Não existem itens cadastrados.')

def interface_relatorio_estoque_minimo(arquivo_itens, arquivo_movimentacoes):
    estoque = dados_estoque(arquivo_itens, arquivo_movimentacoes)
    qtd_itens = 0
    qtd_itens_sem_estoque = 0
    qtd_itens_reposição = 0
    estoque.sort(key=lambda item: item['nome'])
    cabecalho_relatorio_estoque()
    for item in estoque:
        if item['quantidade'] <= item['estoque_minimo'] + (item['estoque_minimo'] * 20 / 100):
            qtd_itens += 1
            print(f'{item["id_item"]:<10}'
                  f'{item["nome"]:<50}'
                  f'{item["un_med"]:<10}'
                  f'{item["quantidade"]:<10}'
                  f'{item["estoque_minimo"]:<10}'
                  f'{formatar_para_real(item["preco_un"]):<15}'
                  f'{formatar_para_real(item["valor_total"]):<15}', end='')
            if item['status'] == 'REPOSIÇÃO':
                qtd_itens_reposição += 1
                print(f'{cores["vm"]}{item["status"]:<10}{cores["limpa"]}')
            elif item['status'] == 'ATENÇÃO':
                print(f'{cores["am"]}{item["status"]:<10}{cores["limpa"]}')
            elif item['status'] == 'SEM ESTOQUE':
                qtd_itens_sem_estoque += 1
                print(f'{cores["vm"]}{item["status"]:<10}{cores["limpa"]}')
    separador()
    resumo = (
        f'{cores["negrito"]}Itens listados: {cores["limpa"]}{qtd_itens} | '
        f'{cores["negrito"]}Sem estoque: {cores["limpa"]}{qtd_itens_sem_estoque} | '
        f'{cores["negrito"]}Para reposição: {cores["limpa"]}{qtd_itens_reposição} '
    )
    print(resumo.center(130))
    separador()