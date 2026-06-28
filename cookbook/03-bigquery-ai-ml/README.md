# 03 · Skill `bigquery-ai-ml` — ML e LLM dentro do warehouse

## O que a skill faz
A skill [`bigquery-ai-ml`](https://github.com/google/skills/blob/main/skills/cloud/bigquery-ai-ml/SKILL.md)
ensina o agente a fazer **machine learning direto no SQL do BigQuery** (BQML): treinar modelos com
`CREATE MODEL`, prever séries temporais com **`ML.FORECAST`** (ARIMA_PLUS) e até chamar o **Gemini dentro
do SQL** com **`ML.GENERATE_TEXT`** — sem mover os dados para fora do warehouse.

## Como rodamos de graça aqui
BQML roda no BigQuery (precisa de projeto GCP). Para o exemplo rodar **local e sem custo**, o
[`example.py`](example.py) faz o **equivalente** com uma regressão linear simples em `numpy` sobre a
receita mensal — a mesma ideia do `ML.FORECAST` em pequena escala. O SQL real do BigQuery está em
[`bqml.sql`](bqml.sql) como referência.

## Instale a skill no seu agente
```bash
npx skills add google/skills
# selecione: cloud/bigquery-ai-ml
```

## Cole no Claude Code / Cursor
> Usando a skill **bigquery-ai-ml**, gere o SQL BQML para: (1) treinar um modelo `ARIMA_PLUS` de previsão
> da receita mensal a partir da tabela `vendas`, (2) prever os próximos 2 meses com `ML.FORECAST` e (3)
> resumir a tendência com `ML.GENERATE_TEXT` (Gemini). Além disso, gere um `example.py` que faça uma
> previsão equivalente local com numpy, para eu testar sem um projeto GCP.

## Rode o exemplo
```bash
pip install -r ../../requirements.txt        # uma vez
python example.py
```

## Saída esperada
```
=== Receita mensal (historico) ===
  2026-01: R$ 34.590,00
  2026-02: R$ 41.850,00
  2026-03: R$ 68.990,00

Tendencia detectada: alta (~R$ 17.200,00 por mes)

=== Previsao dos proximos 2 meses ===
  2026-04: R$ 82.876,67  (previsto)
  2026-05: R$ 100.076,67 (previsto)
```

## O equivalente no BigQuery real
Veja [`bqml.sql`](bqml.sql) — treino com `CREATE MODEL ... ARIMA_PLUS`, previsão com `ML.FORECAST`, e
LLM-no-SQL com `ML.GENERATE_TEXT`. É o "de verdade" do que o `example.py` aproxima localmente.
