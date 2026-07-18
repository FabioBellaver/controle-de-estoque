import json
import os

#itens
def criar_arquivo_itens(nome_arquivo_itens):
    if not os.path.exists(nome_arquivo_itens):
        with open(nome_arquivo_itens, 'w', encoding="utf-8") as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)

def ler_arquivo_itens(nome_arquivo_itens):
    if not os.path.exists(nome_arquivo_itens):
        criar_arquivo_itens(nome_arquivo_itens)
    with open(nome_arquivo_itens, 'r', encoding="utf-8") as arquivo:
        dados_itens = json.load(arquivo)
        return dados_itens

def salvar_arquivo_itens(nome_arquivo_itens, itens):
        with open(nome_arquivo_itens, 'w', encoding='utf-8') as arquivo:
            json.dump(itens, arquivo, indent=4, ensure_ascii=False)

#movimentacoes
def criar_arquivo_movimentacoes(nome_arquivo_movimentacoes):
    if not os.path.exists(nome_arquivo_movimentacoes):
        with open(nome_arquivo_movimentacoes, 'w', encoding="utf-8") as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)

def ler_arquivo_movimentacoes(nome_arquivo_movimentacoes):
    if not os.path.exists(nome_arquivo_movimentacoes):
        criar_arquivo_movimentacoes(nome_arquivo_movimentacoes)
    with open(nome_arquivo_movimentacoes, 'r', encoding="utf-8") as arquivo:
        dados_movimentacoes = json.load(arquivo)
        return dados_movimentacoes

def salvar_arquivo_movimentacoes(nome_arquivo_movimentacoes, registro):
    with open(nome_arquivo_movimentacoes, 'w', encoding="utf-8") as arquivo:
        json.dump(registro, arquivo, indent=4, ensure_ascii=False)
