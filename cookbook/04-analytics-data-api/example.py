"""
Receita 04 - Skill `google-analytics-data-api-basics`
=====================================================
Le um relatorio do Google Analytics 4 (GA4) e calcula metricas por canal:
sessoes, usuarios, conversoes e taxa de conversao.

Para rodar local e de graca, lemos `sample_ga4.json`, que tem EXATAMENTE o mesmo
formato da resposta da Data API (dimensionHeaders / metricHeaders / rows). Assim,
a funcao `relatorio_para_dataframe()` funciona igual com a API real - veja o
trecho comentado em `main()`.

Rode:  python example.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

JSON = Path(__file__).parent / "sample_ga4.json"


def relatorio_para_dataframe(relatorio: dict) -> pd.DataFrame:
    """Converte a resposta do GA4 (runReport) em um DataFrame.

    Funciona tanto com o JSON de exemplo quanto com a resposta real da API,
    pois ambos tem a mesma estrutura: cabecalhos + linhas com dimensionValues
    e metricValues.
    """
    dimensoes = [h["name"] for h in relatorio["dimensionHeaders"]]
    metricas = [h["name"] for h in relatorio["metricHeaders"]]

    registros = []
    for linha in relatorio["rows"]:
        valores = {d: dv["value"] for d, dv in zip(dimensoes, linha["dimensionValues"])}
        for m, mv in zip(metricas, linha["metricValues"]):
            valores[m] = int(mv["value"])  # metricas inteiras neste relatorio
        registros.append(valores)
    return pd.DataFrame(registros)


def main() -> None:
    relatorio = json.loads(JSON.read_text(encoding="utf-8"))

    # --- Para buscar da API REAL do GA4 (em vez do JSON de exemplo) ---
    # from google.analytics.data_v1beta import BetaAnalyticsDataClient
    # from google.analytics.data_v1beta.types import (
    #     RunReportRequest, Dimension, Metric, DateRange,
    # )
    # client = BetaAnalyticsDataClient()
    # resposta = client.run_report(RunReportRequest(
    #     property=f"properties/{SEU_PROPERTY_ID}",
    #     dimensions=[Dimension(name="sessionDefaultChannelGroup")],
    #     metrics=[Metric(name="sessions"), Metric(name="activeUsers"), Metric(name="conversions")],
    #     date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    # ))
    # relatorio = type(resposta).to_dict(resposta)  # mesma estrutura do JSON de exemplo

    df = relatorio_para_dataframe(relatorio)
    df = df.rename(columns={"sessionDefaultChannelGroup": "canal"})
    df["taxa_conversao_%"] = (df["conversions"] / df["sessions"] * 100).round(2)
    df = df.sort_values("sessions", ascending=False)

    print("=== Desempenho por canal (GA4) ===")
    print(df.to_string(index=False))

    total_sessoes = df["sessions"].sum()
    melhor = df.loc[df["taxa_conversao_%"].idxmax()]
    print(f"\nTotal de sessoes: {total_sessoes:,}")
    print(f"Melhor taxa de conversao: {melhor['canal']} ({melhor['taxa_conversao_%']}%)")


if __name__ == "__main__":
    main()
