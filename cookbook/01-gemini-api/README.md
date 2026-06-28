# 01 · Skill `gemini-api` — insights de vendas com o Gemini

## O que a skill faz
A skill [`gemini-api`](https://github.com/google/skills/blob/main/skills/cloud/gemini-api/SKILL.md)
ensina o agente a usar o **SDK novo e unificado `google-genai`** para chamar o Gemini — tanto pela
**Gemini Developer API** (chave gratuita do AI Studio) quanto pela **Vertex AI / Agent Platform**.
Ela cobre geração de texto, entradas multimodais, saída estruturada, embeddings e mais — sempre
recomendando autenticação por variável de ambiente e os modelos atuais.

## Instale a skill no seu agente
```bash
npx skills add google/skills
# selecione: cloud/gemini-api
```
(Passo a passo completo para Claude Code e Cursor em [`../../docs/SKILLS-INSTALL.md`](../../docs/SKILLS-INSTALL.md).)

## Cole no Claude Code / Cursor
> Usando a skill **gemini-api**, crie um `example.py` que lê `vendas.csv` com pandas, resume a receita
> por produto/categoria/mês e gera **3 insights de negócio** em português usando o SDK `google-genai`.
> Leia a chave de `GOOGLE_API_KEY` e o modelo de `GEMINI_MODEL`. Inclua um **modo mock** que funciona
> sem chave (resposta determinística a partir dos dados).

## Rode o exemplo
```bash
pip install -r ../../requirements.txt        # uma vez
python example.py
```

**Sem chave** → modo mock (offline). **Com chave** (cole sua `GOOGLE_API_KEY` no `.env` da raiz) →
insights reais do Gemini. Pegue uma chave gratuita em https://aistudio.google.com/apikey.

## Saída esperada (modo mock)
```
=== Resumo dos dados ===
Receita total: R$ 145.430,00
Receita por produto:
  - Notebook Pro: R$ 72.000,00
  ...
=== Insights do Gemini ===
1. O carro-chefe em receita e Notebook Pro: ...
2. A receita cresce mes a mes; ...
3. Eletronicos puxam o faturamento, mas Acessorios tem alto volume ...
```

## Pontos-chave (o que a skill recomenda)
- Use **`google-genai`** (`from google import genai`) — **não** o legado `google-generativeai`.
- Autentique por **variável de ambiente**, nunca com a chave no código.
- Use um **modelo atual** (`GEMINI_MODEL`), não fixe uma versão antiga.
- Para enterprise, troque para Vertex: `genai.Client(vertexai=True, project=..., location=...)`.
