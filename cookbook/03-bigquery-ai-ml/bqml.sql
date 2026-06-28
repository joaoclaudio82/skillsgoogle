-- SQL de REFERENCIA do BigQuery ML (BQML) - como a previsao e o uso de LLM ficam
-- quando rodam de verdade no BigQuery. O example.py faz o equivalente local em numpy.
-- Substitua `seu_projeto.vendas` pelo seu dataset/tabela.

-- 1) Treina um modelo de previsao de series temporais (ARIMA_PLUS) sobre a receita mensal.
CREATE OR REPLACE MODEL `seu_projeto.vendas.modelo_receita`
OPTIONS (
  model_type            = 'ARIMA_PLUS',
  time_series_timestamp_col = 'mes',
  time_series_data_col      = 'receita'
) AS
SELECT
  DATE_TRUNC(CAST(data AS DATE), MONTH) AS mes,
  SUM(receita)                          AS receita
FROM `seu_projeto.vendas.vendas`
GROUP BY mes;

-- 2) Preve os proximos 2 meses (com intervalo de confianca).
SELECT *
FROM ML.FORECAST(
  MODEL `seu_projeto.vendas.modelo_receita`,
  STRUCT(2 AS horizon, 0.9 AS confidence_level)
);

-- 3) LLM dentro do SQL: usa o Gemini (modelo remoto) para resumir os numeros.
--    Requer um modelo remoto criado com CREATE MODEL ... REMOTE WITH CONNECTION.
SELECT
  ml_generate_text_result
FROM ML.GENERATE_TEXT(
  MODEL `seu_projeto.vendas.gemini`,
  (
    SELECT CONCAT(
      'Resuma em 2 frases a tendencia de receita: ',
      STRING_AGG(FORMAT('%t: %.2f', mes, receita), ', ')
    ) AS prompt
    FROM (
      SELECT DATE_TRUNC(CAST(data AS DATE), MONTH) AS mes, SUM(receita) AS receita
      FROM `seu_projeto.vendas.vendas`
      GROUP BY mes
    )
  ),
  STRUCT(0.2 AS temperature, 256 AS max_output_tokens)
);
