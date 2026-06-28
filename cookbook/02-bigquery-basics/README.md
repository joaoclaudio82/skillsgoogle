# 02 · Skill `bigquery-basics` — warehouse e SQL analítico

## O que a skill faz
A skill [`bigquery-basics`](https://github.com/google/skills/blob/main/skills/cloud/bigquery-basics/SKILL.md)
ensina o agente o essencial do **BigQuery**, o data warehouse serverless do Google: criar datasets e
tabelas, carregar dados e rodar **consultas analíticas** (agregações, filtros, joins) com SQL padrão.

## Como rodamos de graça aqui
BigQuery real exige um projeto GCP. Para o exemplo rodar **local e sem custo**, usamos o **DuckDB** como
stand-in: o **mesmo SQL** de [`queries.sql`](queries.sql) roda no DuckDB e no BigQuery (usamos só funções
padrão como `SUM`, `AVG`, `GROUP BY`, `EXTRACT`). Trocar para o BigQuery real é uma linha — veja o
comentário em `consultar()` no [`example.py`](example.py).

## Instale a skill no seu agente
```bash
npx skills add google/skills
# selecione: cloud/bigquery-basics
```

## Cole no Claude Code / Cursor
> Usando a skill **bigquery-basics**, escreva consultas SQL analíticas sobre uma tabela `vendas`
> (colunas: data, produto, categoria, quantidade, preco_unitario, receita): receita total, receita por
> produto, receita por mês (com `EXTRACT`) e ticket médio por categoria. Use só SQL padrão que rode tanto
> no BigQuery quanto no DuckDB, e um `example.py` que carrega o `vendas.csv` e executa cada consulta.

## Rode o exemplo
```bash
pip install -r ../../requirements.txt        # uma vez
python example.py
```

## Saída esperada (trecho)
```
Tabela `vendas` criada com 16 linhas.

=== receita_por_produto ===
         produto  receita  unidades
    Notebook Pro  72000.0      16.0
      Monitor 24  38950.0      41.0
Teclado Mecanico  24640.0      77.0
   Mouse Sem Fio   9840.0     123.0
```

## Do DuckDB para o BigQuery real (1 linha)
```python
# Local (este exemplo):
con.execute(sql).fetchdf()

# BigQuery real:
from google.cloud import bigquery
client = bigquery.Client(project="SEU_PROJETO")
client.query(sql).to_dataframe()
```
Dica: o **BigQuery Sandbox** (https://cloud.google.com/bigquery/docs/sandbox) deixa você consultar
datasets públicos **sem cartão de crédito**.
