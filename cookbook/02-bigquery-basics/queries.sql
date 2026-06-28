-- Consultas analiticas sobre a tabela `vendas`.
-- Usam apenas SQL padrao (SUM, AVG, GROUP BY, EXTRACT), entao rodam IGUAL no
-- DuckDB (local, neste exemplo) e no BigQuery. Cada bloco e nomeado com "-- name:".

-- name: receita_total
SELECT ROUND(SUM(receita), 2) AS receita_total
FROM vendas;

-- name: receita_por_produto
SELECT produto,
       ROUND(SUM(receita), 2) AS receita,
       SUM(quantidade)        AS unidades
FROM vendas
GROUP BY produto
ORDER BY receita DESC;

-- name: receita_por_mes
SELECT EXTRACT(YEAR  FROM CAST(data AS DATE)) AS ano,
       EXTRACT(MONTH FROM CAST(data AS DATE)) AS mes,
       ROUND(SUM(receita), 2)                 AS receita
FROM vendas
GROUP BY ano, mes
ORDER BY ano, mes;

-- name: ticket_medio_por_categoria
SELECT categoria,
       ROUND(AVG(receita), 2) AS ticket_medio,
       SUM(quantidade)        AS itens_vendidos
FROM vendas
GROUP BY categoria
ORDER BY ticket_medio DESC;
