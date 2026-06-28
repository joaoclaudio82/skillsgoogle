"""
Receita 03 - Skill `bigquery-ai-ml`
===================================
Mostra a ideia de "ML dentro do warehouse": treinar um modelo de previsao de
series temporais a partir das vendas e prever os proximos meses.

No BigQuery isso seria `CREATE MODEL ... ML.FORECAST` (ARIMA_PLUS) - veja
`bqml.sql`. Para rodar local e de graca, fazemos o equivalente com uma regressao
linear simples (numpy) sobre a receita mensal.

Rode:  python example.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "vendas.csv"
HORIZONTE = 2  # quantos meses prever


def receita_mensal(df: pd.DataFrame) -> pd.Series:
    """Soma a receita por mes (indexada por periodo mensal)."""
    periodo = pd.to_datetime(df["data"]).dt.to_period("M")
    return df.groupby(periodo)["receita"].sum()


def prever(serie: pd.Series, horizonte: int) -> pd.Series:
    """Ajusta uma reta (minimos quadrados) e projeta `horizonte` meses a frente.

    Equivale, em pequena escala, ao que o BQML ML.FORECAST faz no BigQuery.
    """
    x = np.arange(len(serie))
    coef = np.polyfit(x, serie.to_numpy(), 1)  # regressao linear: a*x + b
    modelo = np.poly1d(coef)

    futuros_x = np.arange(len(serie), len(serie) + horizonte)
    meses_futuros = pd.period_range(serie.index[-1] + 1, periods=horizonte, freq="M")
    valores = np.maximum(modelo(futuros_x), 0).round(2)  # receita nao fica negativa
    return pd.Series(valores, index=meses_futuros), coef


def main() -> None:
    df = pd.read_csv(CSV)
    serie = receita_mensal(df)

    print("=== Receita mensal (historico) ===")
    for mes, valor in serie.items():
        print(f"  {mes}: R$ {valor:,.2f}")

    previsao, (inclinacao, intercepto) = prever(serie, HORIZONTE)
    tendencia = "alta" if inclinacao > 0 else "queda" if inclinacao < 0 else "estavel"

    print(f"\nTendencia detectada: {tendencia} (~R$ {inclinacao:,.2f} por mes)")
    print(f"\n=== Previsao dos proximos {HORIZONTE} meses ===")
    for mes, valor in previsao.items():
        print(f"  {mes}: R$ {valor:,.2f}  (previsto)")

    print("\nNo BigQuery real, o mesmo resultado sai de ML.FORECAST - veja bqml.sql.")


if __name__ == "__main__":
    main()
