# Como instalar as Google Skills no Claude Code e no Cursor

As [Agent Skills do Google](https://github.com/google/skills) são instaladas com o CLI aberto
**`skills`** (da vercel-labs), que funciona com Claude Code, Cursor, Codex, Gemini CLI e 30+ agentes.

## Pré-requisito
- **Node.js** instalado (verifique com `node --version`). Baixe em https://nodejs.org se precisar.

## Instalação (interativa)
No terminal, **dentro da pasta do seu projeto**:

```bash
npx skills add google/skills
```

Você verá uma lista para **selecionar quais skills** instalar. Para este cookbook, escolha:

- `cloud/gemini-api`
- `cloud/bigquery-basics`
- `cloud/bigquery-ai-ml`
- `analytics/google-analytics-data-api-basics`

## Escolhendo o agente
Por padrão o CLI detecta seu agente. Para mirar agentes específicos use `--agent`:

```bash
# Claude Code
npx skills add google/skills --agent claude-code

# Cursor
npx skills add google/skills --agent cursor

# os dois de uma vez
npx skills add google/skills --agent claude-code cursor
```

## Onde as skills ficam
Os arquivos `SKILL.md` são copiados para a pasta de config do agente, por exemplo:

| Agente | Pasta |
|--------|-------|
| Claude Code | `.claude/skills/` |
| Genérico / outros | `.agents/skills/` |

A partir daí o agente "enxerga" a skill e passa a seguir as orientações dela quando o assunto aparece.

> Neste repositório, `.claude/` e `.cursor/` estão no `.gitignore` — as skills instaladas localmente
> não são versionadas; cada pessoa instala as suas com o comando acima.

## Comandos úteis do CLI
```bash
npx skills list           # lista skills instaladas
npx skills add <fonte>    # instala de um repo (ex.: google/skills, firebase/agent-skills)
npx skills --help         # todos os comandos
```

## Como usar depois de instalar
Abra o Claude Code ou o Cursor no projeto e **descreva a tarefa** — cada receita deste cookbook traz
**o prompt exato** pra colar. Exemplo (receita 01):

> "Usando a skill **gemini-api**, crie um script que lê `vendas.csv` e gera 3 insights com o Gemini."

O agente vai aplicar as boas práticas da skill (SDK certo, autenticação por env, modelo atual etc.).

---
Fontes: [google/skills](https://github.com/google/skills) · [CLI `skills` (vercel-labs)](https://github.com/vercel-labs/skills)
