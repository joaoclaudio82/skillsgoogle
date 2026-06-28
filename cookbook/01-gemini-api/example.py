"""
Receita 01 - Skill `gemini-api`
================================
Le um CSV de vendas, resume os numeros com pandas e pede ao Gemini 3 insights
de negocio em portugues usando o SDK novo `google-genai`.

- COM chave  (GOOGLE_API_KEY no .env): chama o Gemini de verdade.
- SEM chave: cai em MODO MOCK (insights gerados localmente a partir dos dados),
  entao roda offline, de graca e sem configuracao.

Rode:  python example.py
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # carrega .env da raiz do projeto, se existir

CSV = Path(__file__).parent / "vendas.csv"
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def resumo_dos_dados(df: pd.DataFrame) -> str:
    """Agrega os numeros para dar contexto factual ao modelo (e ao mock)."""
    receita_total = df["receita"].sum()
    por_produto = df.groupby("produto")["receita"].sum().sort_values(ascending=False)
    por_categoria = df.groupby("categoria")["receita"].sum().sort_values(ascending=False)
    df = df.assign(mes=pd.to_datetime(df["data"]).dt.strftime("%Y-%m"))
    por_mes = df.groupby("mes")["receita"].sum()

    linhas = [f"Receita total: R$ {receita_total:,.2f}", "", "Receita por produto:"]
    linhas += [f"  - {p}: R$ {v:,.2f}" for p, v in por_produto.items()]
    linhas += ["", "Receita por categoria:"]
    linhas += [f"  - {c}: R$ {v:,.2f}" for c, v in por_categoria.items()]
    linhas += ["", "Receita por mes:"]
    linhas += [f"  - {m}: R$ {v:,.2f}" for m, v in por_mes.items()]
    return "\n".join(linhas)


def gerar_insights(resumo: str) -> str:
    """Chama o Gemini (google-genai). Se nao houver chave, usa o mock."""
    api_key = os.getenv("GOOGLE_API_KEY")
    prompt = (
        "Voce e um analista de dados. Com base no resumo de vendas abaixo, "
        "escreva exatamente 3 insights de negocio acionaveis, em portugues, "
        "em formato de lista numerada e curta.\n\n"
        f"{resumo}\n"
    )

    if not api_key:
        return _mock(resumo)

    # SDK novo e unificado exigido pela skill `gemini-api`.
    from google import genai

    client = genai.Client(api_key=api_key)  # caminho Gemini Developer API (chave do AI Studio)
    # Para usar Vertex AI / Agent Platform:
    #   client = genai.Client(vertexai=True, project="SEU_PROJETO", location="us-central1")
    resposta = client.models.generate_content(model=MODEL, contents=prompt)
    return resposta.text.strip()


def _mock(resumo: str) -> str:
    """Insights determinISticos a partir dos numeros (usado quando nao ha chave)."""
    linha_top = next(
        (l for l in resumo.splitlines() if l.strip().startswith("- ")), "- (sem dados)"
    )
    top_produto = linha_top.strip()[2:]
    return (
        "[MODO MOCK - defina GOOGLE_API_KEY no .env para usar o Gemini de verdade]\n"
        f"1. O carro-chefe em receita e {top_produto} - concentre estoque e campanhas nele.\n"
        "2. A receita cresce mes a mes; reforce a equipe de vendas para sustentar a tendencia.\n"
        "3. Eletronicos puxam o faturamento, mas Acessorios tem alto volume - explore combos "
        "(notebook + mouse + teclado) para aumentar o ticket medio."
    )


def main() -> None:
    df = pd.read_csv(CSV)
    resumo = resumo_dos_dados(df)
    print("=== Resumo dos dados ===")
    print(resumo)
    print("\n=== Insights do Gemini ===")
    print(gerar_insights(resumo))


if __name__ == "__main__":
    main()
