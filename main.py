from lib.arquivos import criar_arquivo_itens, criar_arquivo_movimentacoes, ler_arquivo_itens, ler_arquivo_movimentacoes
from lib.interfaces import titulo_app, menu_principal, titulo, interface_cadastrar_item, interface_registrar_entrada, \
    interface_registrar_saida, interface_relatorio_estoque, \
    interface_historico_movimentacoes, interface_relatorio_estoque_minimo, interface_relatorio_por_consumo
from lib.uteis import validar_opcao

arquivo_itens = 'arquivos/itens.json'
arquivo_movimentacoes = 'arquivos/movimentacoes.json'
criar_arquivo_itens(arquivo_itens)
criar_arquivo_movimentacoes(arquivo_movimentacoes)

ler_arquivo_itens(arquivo_itens)
ler_arquivo_movimentacoes(arquivo_movimentacoes)

titulo_app('Controle de estoque')

while True:
    menu_principal()
    opcao = validar_opcao(8)
    if opcao == 1:
        titulo('Cadastrar item')
        interface_cadastrar_item(arquivo_itens)
    elif opcao == 2:
        titulo('Registrar entrada de estoque')
        interface_registrar_entrada(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 3:
        titulo('Registrar saída (requisição)')
        interface_registrar_saida(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 4:
        titulo('Listar itens (com quantidade atual e status)')
        interface_relatorio_estoque(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 5:
        titulo('Histórico de movimentação de um item')
        interface_historico_movimentacoes(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 6:
        titulo('Itens com estoque crítico')
        interface_relatorio_estoque_minimo(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 7:
        titulo('Relatório de consumo por setor')
        interface_relatorio_por_consumo(arquivo_itens, arquivo_movimentacoes)
    elif opcao == 8:
        break

titulo_app('Sistema encerrado')
