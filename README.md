# Sistema de Almoxarifado

Um sistema em Python para controle de estoque por movimentação (entradas e saídas), com dois arquivos JSON relacionados como banco de dados.

## Funcionalidades

- Cadastrar itens, com estoque mínimo
- Registrar entradas e saídas de estoque (a quantidade atual é sempre calculada a partir do histórico, nunca armazenada fixa)
- Bloquear saídas maiores que o estoque disponível
- Listar itens com status (OK, atenção, reposição, sem estoque)
- Ver histórico de movimentação de um item
- Gerar relatório de consumo por setor

## Tecnologias

- Python
- JSON
- nanoid

## Executando o Projeto

Instale a dependência necessária:

```bash
pip install nanoid
```

Execute o projeto:

```bash
python main.py
```

## Autor

Fabio Bellaver
