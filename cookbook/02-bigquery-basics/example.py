"""
Receita 02 - Skill `bigquery-basics`
====================================
Demonstra o basico de um data warehouse: criar uma tabela a partir de um CSV e
rodar consultas analiticas (agregacoes) sobre ela.

Para rodar 100% local e de graca, usamos o DuckDB como "stand-in" do BigQuery:
o MESMO SQL de `queries.sql` roda nos dois. O trecho para usar o BigQuery real
esta comentado em `consultar()`.

Rode:  python example.py
"""
from __future__ import annotations

from pathlib import Path

import duckdb

HERE = Path(__file__).parent
CSV = HERE / "vendas.csv"
QUERIES = HERE / "queries.sql"


def carregar_queries(path: Path) -> dict[str, str]:
    """Le queries.sql e separa os blocos marcados por `-- name: <nome>`."""
    blocos: dict[str, str] = {}
    nome: str | None = None
    buffer: list[str] = []
    for linha in path.read_text(encoding="utf-8").splitlines():
        if linha.strip().lower().startswith("-- name:"):
            if nome:
                blocos[nome] = "\n".join(buffer).strip()
            nome = linha.split(":", 1)[1].strip()
            buffer = []
        elif nome is not None:
            buffer.append(linha)
    if nome:
        blocos[nome] = "\n".join(buffer).strip()
    return blocos


def consultar(con: duckdb.DuckDBPyConnection, sql: str):
    """Executa um SELECT e devolve um DataFrame.

    Para usar o BigQuery REAL, troque por:
        from google.cloud import bigquery
        client = bigquery.Client(project="SEU_PROJETO")
        return client.query(sql).to_dataframe()
    """
    return con.execute(sql).fetchdf()


def main() -> None:
    con = duckdb.connect()  # warehouse local em memoria
    # Carrega o CSV em uma tabela chamada `vendas`.
    # No BigQuery isso seria um `bq load` ou um `LOAD DATA` para uma tabela do dataset.
    con.execute(
        f"CREATE TABLE vendas AS SELECT * FROM read_csv_auto('{CSV.as_posix()}')"
    )
    print(f"Tabela `vendas` criada com {con.execute('SELECT COUNT(*) FROM vendas').fetchone()[0]} linhas.\n")

    for nome, sql in carregar_queries(QUERIES).items():
        print(f"=== {nome} ===")
        print(consultar(con, sql).to_string(index=False))
        print()


if __name__ == "__main__":
    main()
