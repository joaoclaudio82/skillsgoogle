# Google Skills Cookbook 🍳

Exemplos **curtos e práticos** de como usar as [**Agent Skills oficiais do Google**](https://github.com/google/skills)
no **Claude Code** e no **Cursor** — com foco em **dados e machine learning**.

Cada receita mostra:
1. **O que a skill faz**
2. **Como instalar** a skill no seu agente
3. **O prompt exato** pra colar no Claude/Cursor
4. Um **exemplo Python rodável** (local e grátis)

> Tudo roda **localmente e de graça**. Sem chave de API, os exemplos caem em **modo mock**
> (resposta simulada) e funcionam offline. Com uma chave gratuita do
> [Google AI Studio](https://aistudio.google.com/apikey), você vê o Gemini de verdade.

---

## O que são "Agent Skills"?

São arquivos `SKILL.md` (instruções + boas práticas) que ensinam um agente de IA a usar um
produto Google corretamente. Você instala com **um comando** e o agente passa a "saber" usar
aquela tecnologia. O repositório [`google/skills`](https://github.com/google/skills) tem hoje
**65 skills** (Google Cloud, Ads e Analytics).

```bash
npx skills add google/skills
```

Veja o passo a passo de instalação no Claude Code e no Cursor em
[`docs/SKILLS-INSTALL.md`](docs/SKILLS-INSTALL.md).

---

## As receitas (tema: dados / ML)

| # | Receita | Skill do Google | O que o exemplo faz |
|---|---------|-----------------|---------------------|
| 01 | [Gemini API](cookbook/01-gemini-api/) | `cloud/gemini-api` | Lê um CSV de vendas e gera 3 insights de negócio com o Gemini |
| 02 | [BigQuery Basics](cookbook/02-bigquery-basics/) | `cloud/bigquery-basics` | "Data warehouse" local (DuckDB) com agregações SQL |
| 03 | [BigQuery AI/ML](cookbook/03-bigquery-ai-ml/) | `cloud/bigquery-ai-ml` | Previsão simples de vendas + SQL BQML de referência |
| 04 | [Analytics Data API](cookbook/04-analytics-data-api/) | `analytics/google-analytics-data-api-basics` | Processa métricas GA4 de exemplo por canal |

---

## Começando

```bash
# 1) Instale as dependências
pip install -r requirements.txt

# 2) (Opcional) configure sua chave gratuita do Gemini
cp .env.example .env
# edite .env e cole sua GOOGLE_API_KEY

# 3) Rode qualquer receita
python cookbook/01-gemini-api/example.py
```

---

## Estrutura

```
.
├── README.md
├── requirements.txt
├── .env.example
├── docs/
│   └── SKILLS-INSTALL.md
└── cookbook/
    ├── 01-gemini-api/
    ├── 02-bigquery-basics/
    ├── 03-bigquery-ai-ml/
    └── 04-analytics-data-api/
```

## Licença

MIT.
