# Manutenção da skill

Para quem mantém o pacote. O Claude não precisa deste arquivo para executar
um atendimento.

## Sumário

- [Princípio de organização](#principio-de-organizacao)
- [Estrutura](#estrutura)
- [Claude Code](#claude-code)
- [App claude.ai](#app-claudeai)
- [Dependências opcionais](#dependencias-opcionais)
- [Ao alterar uma regra](#ao-alterar-uma-regra)

## Princípio de organização

Uma regra tem **um** dono. As regras clínicas moram só em `fases/`; os
arquivos em `.claude/agents/` são invólucros finos que mandam ler a fase
correspondente. Assim uma mudança é feita num lugar só e vale para os dois
ambientes, sem risco das versões divergirem.

O que separa `fases/` de `referencia/` é a frequência de uso, não a
importância: `fases/` é lido em todo atendimento, `referencia/` só quando a
condição específica aparece. Conteúdo que sempre será necessário não deve ir
para `referencia/` — o salto de leitura extra não compraria nada.

## Estrutura

```
nutri-orquestrador/
  SKILL.md              orquestrador: mapa de arquivos, fluxo, checklist
  HANDOFF.md            contrato JSON entre as fases
  MANUTENCAO.md         este arquivo
  fases/                REGRAS CLÍNICAS — lidas em todo atendimento
    00-anamnese.md      05-auditoria.md etc.
  referencia/           carregado só quando a condição aparece
    modos-especiais.md  se o modo for pre_pos_treino ou competicao
    evidencias.md       se questionarem o porquê de uma regra
    troubleshooting.md  se uma fase falhar ou não convergir
    incorporar-material.md  ao processar entrada/
  scripts/
    validar_plano.py    executado, não lido
  evals/                três cenários + como rodar
```

Fora da skill, no repositório: `entrada/` (materiais novos a incorporar) e
`.claude/agents/nutri-*.md` (só Claude Code).

## Claude Code

Funciona direto, sem instalação. A skill detecta a ferramenta `Agent` e os
arquivos `.claude/agents/nutri-*.md` e entra em **Modo Code**:

- Exames ‖ cálculo em paralelo; suplementação ‖ prescrição em paralelo.
- Cada especialista tem contexto próprio e limpo.
- O `tools:` de cada agente limita o que ele faz: o auditor não tem
  `Write`/`Edit`, então não consegue "consertar" o plano nem se quisesse.

## App claude.ai

Suba como Skill pessoal a pasta `nutri-orquestrador/` inteira. **Não** suba
`.claude/agents/`: lá não há despacho para subagentes, e a skill detecta
isso e entra em **Modo App**, executando as mesmas fases sequencialmente a
partir dos mesmos arquivos.

Perde-se paralelismo e o isolamento de contexto do auditor. A fase de
auditoria compensa em parte exigindo o validador e as contas refeitas item a
item, mas um auditor que também montou o plano é estruturalmente menos
rigoroso. Para caso complexo, prefira o Claude Code.

## Dependências opcionais

As fases procuram, e usam quando existirem:

- `scripts/calculo_metabolico.py`, `meal_engine.py`,
  `substitution_engine.py`, `regulatory_gate.py` (do NutriPlanner)
- `knowledge_base/tables/alimentos.json` (TACO) e `TBCA_POLICY.md`
- `knowledge_base/references/EVIDENCE_POLICY.md` e `evidence_registry.json`
- `calculos.json` (tolerâncias) e `assets/template_dieta.md`

Sem esses arquivos o sistema **não quebra**: cada fase cai para o modo
manual, mostra a conta por extenso e registra a limitação. `validar_plano.py`
usa os padrões declarados no próprio script quando `calculos.json` não
existe, e diz no cabeçalho da saída qual origem usou.

Exceção: `regulatory_gate.py` ausente **não** libera suplemento — sem gate a
política fica mais estrita, não mais frouxa.

## Ao alterar uma regra

1. Edite o arquivo em `fases/` (ou `referencia/`, se for condicional).
2. Se a auditoria precisa conferir a regra nova, atualize o checklist em
   `fases/05-auditoria.md`. Regra que a auditoria não confere é regra que na
   prática não existe.
3. Se a regra é aritmética verificável, estenda `scripts/validar_plano.py`.
4. Se criou arquivo novo em `referencia/`, registre a linha no mapa de
   arquivos do `SKILL.md` — arquivo que não está no mapa não é lido.
5. Rode os evals antes do commit.

Mantenha `SKILL.md` abaixo de 500 linhas. Passou disso, mova conteúdo para
`referencia/`.
