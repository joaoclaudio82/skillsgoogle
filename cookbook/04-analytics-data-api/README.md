# 04 · Skill `google-analytics-data-api-basics` — métricas do GA4

## O que a skill faz
A skill [`google-analytics-data-api-basics`](https://github.com/google/skills/blob/main/skills/analytics/google-analytics-data-api-basics/SKILL.md)
ensina o agente a consultar a **Google Analytics Data API (GA4)**: montar um `runReport` com **dimensões**
(ex.: canal, país, página) e **métricas** (sessões, usuários, conversões) e transformar a resposta em
dados prontos para análise.

## Como rodamos de graça aqui
A API real precisa de uma propriedade GA4 e credenciais. Para rodar **local e sem custo**, lemos
[`sample_ga4.json`](sample_ga4.json), que tem **exatamente o mesmo formato** da resposta da API
(`dimensionHeaders` / `metricHeaders` / `rows`). Por isso a função `relatorio_para_dataframe()` do
[`example.py`](example.py) funciona **igual** com a API real — basta descomentar o trecho do cliente.

## Instale a skill no seu agente
```bash
npx skills add google/skills
# selecione: analytics/google-analytics-data-api-basics
```

## Cole no Claude Code / Cursor
> Usando a skill **google-analytics-data-api-basics**, escreva um `example.py` que faça um `runReport`
> do GA4 com a dimensão `sessionDefaultChannelGroup` e as métricas `sessions`, `activeUsers` e
> `conversions`, e calcule a taxa de conversão por canal. Faça o parsing funcionar tanto com a resposta
> real quanto com um `sample_ga4.json` de mesmo formato, para eu testar sem uma propriedade GA4.

## Rode o exemplo
```bash
pip install -r ../../requirements.txt        # uma vez
python example.py
```

## Saída esperada
```
=== Desempenho por canal (GA4) ===
         canal  sessions  activeUsers  conversions  taxa_conversao_%
Organic Search      5400         4200          180              3.33
   Paid Search      2200         1980          143              6.50
         Email       610          560           48              7.87
...
Melhor taxa de conversao: Email (7.87%)
```

## Para usar a API real
Descomente o bloco em `main()` (cliente `BetaAnalyticsDataClient`), instale `google-analytics-data`
(está comentado no `requirements.txt`) e autentique com uma conta de serviço com acesso à sua
propriedade GA4. O resto do código não muda — a estrutura da resposta é a mesma do JSON de exemplo.
