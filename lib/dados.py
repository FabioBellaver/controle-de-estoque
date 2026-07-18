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