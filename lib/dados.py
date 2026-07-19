from lib.arquivos import ler_arquivo_itens, salvar_arquivo_itens, ler_arquivo_movimentacoes, \
    salvar_arquivo_movimentacoes


def cadastrar_item(nome_arquivo, item):
    dados_itens = ler_arquivo_itens(nome_arquivo)
    dados_itens.append(item)
    salvar_arquivo_itens(nome_arquivo, dados_itens)


def registrar_entrada(nome_arquivo, registro):
    movimentos = ler_arquivo_movimentacoes(nome_arquivo)
    movimentos.append(registro)
    salvar_arquivo_movimentacoes(nome_arquivo, movimentos)


def registrar_saida(nome_arquivo, registro):
    movimentos = ler_arquivo_movimentacoes(nome_arquivo)
    movimentos.append(registro)
    salvar_arquivo_movimentacoes(nome_arquivo, movimentos)


def dados_estoque(arquivo_itens, arquivo_movimentacoes):
    itens = ler_arquivo_itens(arquivo_itens)
    movimentacoes = (ler_arquivo_movimentacoes(arquivo_movimentacoes))
    relatorio = []
    for item in itens:
        dados_relatorio_estoque = dict()
        dados_relatorio_estoque['quantidade'] = 0
        dados_relatorio_estoque['id_item'] = item['id']
        dados_relatorio_estoque['nome'] = item['nome']
        dados_relatorio_estoque['un_med'] = item['un_med']
        dados_relatorio_estoque['preco_un'] = item['preco']
        dados_relatorio_estoque['estoque_minimo'] = item['estoque_minimo']
        for movimento in movimentacoes:
            if movimento['item_id'] == item['id']:
                if movimento['tipo'] == 'ENTRADA':
                    dados_relatorio_estoque['quantidade'] += movimento['quantidade']
                elif movimento['tipo'] == 'SAIDA':
                    dados_relatorio_estoque['quantidade'] -= movimento['quantidade']
        dados_relatorio_estoque['valor_total'] = dados_relatorio_estoque['quantidade'] * dados_relatorio_estoque[
            'preco_un']
        if dados_relatorio_estoque['quantidade'] == 0:
            dados_relatorio_estoque['status'] = 'SEM ESTOQUE'
        elif dados_relatorio_estoque['quantidade'] < dados_relatorio_estoque['estoque_minimo']:
            dados_relatorio_estoque['status'] = 'REPOSIÇÃO'
        elif dados_relatorio_estoque['quantidade'] <= dados_relatorio_estoque['estoque_minimo'] + (
                dados_relatorio_estoque['estoque_minimo'] * 20 / 100):
            dados_relatorio_estoque['status'] = 'ATENÇÃO'
        else:
            dados_relatorio_estoque['status'] = 'OK'
        relatorio.append(dados_relatorio_estoque)
    return relatorio


def dados_movimentacoes(arquivo_itens, arquivo_movimentacoes):
    itens = ler_arquivo_itens(arquivo_itens)
    movimentos = ler_arquivo_movimentacoes(arquivo_movimentacoes)
    relatorio = []
    for movimentacao in movimentos:
        movimento = dict()
        if movimentacao['tipo'] == 'ENTRADA':
            movimento['id_movimento'] = movimentacao['id']
            movimento['tipo'] = movimentacao['tipo']
            movimento['quantidade'] = movimentacao['quantidade']
            movimento['data'] = movimentacao['data_entrada']
            movimento['setor_requisitante'] = 'N/A'
        elif movimentacao['tipo'] == 'SAIDA':
            movimento['id_movimento'] = movimentacao['id']
            movimento['tipo'] = movimentacao['tipo']
            movimento['quantidade'] = movimentacao['quantidade']
            movimento['data'] = movimentacao['data_saida']
            movimento['setor_requisitante'] = movimentacao['setor_requisitante']
        for item in itens:
            if item['id'] == movimentacao['item_id']:
                movimento['id_item'] = item['id']
                movimento['nome'] = item['nome']
                movimento['un_med'] = item['un_med']
                break
        relatorio.append(movimento)
    return relatorio
