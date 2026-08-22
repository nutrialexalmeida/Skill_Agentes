# nutri-orquestrador — como este pacote funciona nos dois ambientes

## A ideia

As regras clínicas moram **só** em `fases/`. Nada de regra clínica dentro de
`.claude/agents/*.md` — aqueles arquivos são invólucros finos que mandam ler
a fase correspondente. Assim uma mudança de regra é feita em um lugar só e
vale para os dois ambientes, sem risco de as versões divergirem.

```
.claude/skills/nutri-orquestrador/
  SKILL.md              orquestrador; detecta o modo e coordena as fases
  contratos/handoff.md  formato JSON de troca entre as fases
  fases/                AS REGRAS CLÍNICAS (fonte única de verdade)
.claude/agents/nutri-*.md   só no Claude Code; invólucros dos especialistas
```

## Claude Code (potencial máximo)

Funciona direto, sem instalação. A skill detecta que a ferramenta `Agent` e
os arquivos `.claude/agents/nutri-*.md` existem e entra em **Modo Code**:

- Exames e cálculo rodam **em paralelo** (uma onda).
- Suplementação e prescrição rodam **em paralelo** (outra onda).
- Cada especialista tem contexto próprio e limpo — o auditor não vê o
  raciocínio de quem montou o plano, que é o ponto.
- O `tools:` de cada agente limita o que ele pode fazer: o auditor, por
  exemplo, não tem `Write`/`Edit`, então não consegue "consertar" o plano
  mesmo se quisesse.

## App claude.ai (mesmo rigor, sem paralelismo)

Suba como Skill pessoal a pasta `nutri-orquestrador/` inteira — `SKILL.md`,
`fases/` e `contratos/` juntos. **Não** suba `.claude/agents/`: lá não
existe despacho para subagentes, e a skill já detecta isso e entra em
**Modo App**, executando as mesmas fases sequencialmente, lendo os mesmos
arquivos.

O que se perde no app: paralelismo (mais lento) e o isolamento de contexto
do auditor. A fase de auditoria compensa parcialmente exigindo que as contas
sejam refeitas item a item, mas um auditor que também montou o plano é
estruturalmente menos rigoroso que um auditor novo. Para caso complexo,
prefira o Claude Code.

## Dependências opcionais

As fases procuram, e usam quando existirem:

- `scripts/calculo_metabolico.py`, `scripts/meal_engine.py`,
  `scripts/substitution_engine.py`, `scripts/regulatory_gate.py`
- `knowledge_base/tables/alimentos.json` (TACO) e `TBCA_POLICY.md`
- `knowledge_base/references/EVIDENCE_POLICY.md` e `evidence_registry.json`
- `calculos.json` (tolerâncias) e `assets/template_dieta.md`

Sem esses arquivos o sistema **não quebra**: cada fase cai para o modo
manual, mostra a conta por extenso e registra em `observacoes` que o motor
não estava disponível. A tolerância de uniformidade assume 15% como padrão
declarado.

## Ao alterar uma regra

Edite o arquivo em `fases/`. Se a mudança afeta o que a auditoria precisa
conferir, atualize também o checklist em `fases/05-auditoria.md` — uma regra
nova que a auditoria não confere é uma regra que na prática não existe.
