# NutriPlanner-Pro — revisão, portabilidade para Codex e evidências 2024-2026

Atualizado em: 2026-08-22

## Resumo

Usuário pediu para revisar a skill pessoal `nutriplanner-pro` (copiloto de
nutrição, não faz parte deste repositório — é uma skill sincronizada da conta
claude.ai, presente neste ambiente só como
`/root/.claude/skills/synced/nutriplanner-pro/SKILL.md`). Nesta sessão só o
`SKILL.md` estava disponível; `knowledge_base/`, `scripts/` e `assets/` que o
SKILL.md referencia não estavam sincronizados neste ambiente — a revisão de
código/estrutura ficou limitada ao que dá para inferir do `SKILL.md`.

Três entregas foram feitas:
1. Revisão do `SKILL.md` (pontos fortes e sugestões de melhoria).
2. Rascunho de `AGENTS.md` para portar o comportamento para o Codex da
   OpenAI, com as diferenças de mecanismo explicadas (sem trigger por
   intenção, sem hook de reforço por mensagem, sem front-matter funcional).
3. Levantamento de meta-análises/revisões 2024-2026 com amostra grande sobre
   os temas centrais da skill (distribuição de proteína entre refeições,
   dieta hiperproteica e composição corporal, segurança renal de proteína
   alta, distribuição de carboidrato ao longo do dia, equações de GER).

## Decisões e preferências

- Usuário não confirmou explicitamente que "minha skill" = nutriplanner-pro;
  foi a interpretação mais provável dado o contexto (única skill de nutrição
  habilitada, pedido fala de artigos/meta-análises científicas). Se a
  intenção era outra skill, replanejar.
- Entregas de conteúdo (AGENTS.md e evidências) foram mandadas como arquivos
  ao usuário via SendUserFile, não commitadas neste repositório, porque a
  skill nutriplanner-pro não vive neste repositório.

## Trabalho realizado

- 2026-08-22: Lido `SKILL.md` completo da nutriplanner-pro em
  `/root/.claude/skills/synced/nutriplanner-pro/SKILL.md`.
- 2026-08-22: Pesquisa web (WebSearch) de meta-análises 2024-2026 sobre:
  distribuição de proteína entre refeições, dieta hiperproteica e composição
  corporal, segurança renal de proteína alta, cronoNutrição/distribuição de
  carboidrato, equações de gasto energético de repouso, frequência de
  refeições. Fetch de texto completo (WebFetch) bloqueado pelo proxy de rede
  do ambiente para pubmed.ncbi.nlm.nih.gov, nature.com, frontiersin.org e
  pmc.ncbi.nlm.nih.gov — os achados citados vêm dos snippets do buscador, não
  de leitura de texto completo; usuário foi avisado para confirmar antes de
  registrar no evidence_registry.
- 2026-08-22: Gerado e enviado ao usuário `AGENTS.md` (rascunho de
  portabilidade para Codex) e `evidencias_2024-2026.md` (achado por achado,
  com sugestão de nível de evidência e onde encaixar no knowledge_base).

## Achados de revisão principais (para retomar sem reler tudo)

- A regra de "proteína e gordura uniformes entre refeições" (etapa 7 do
  SKILL.md) não tem citação de evidência no próprio arquivo; a literatura
  2024 é mista — sustenta mais a "quantidade mínima por refeição" do que
  uniformidade estrita. Sugestão: registrar como limitação conhecida, manter
  a regra operacional.
- A "pirâmide de carboidrato decrescente ao longo do dia" tem bom respaldo
  recente (JAMA Network Open 2024, 29 RCTs/2.485 participantes: distribuição
  calórica mais cedo no dia associada a maior perda de peso). Vale citar
  essa fonte explicitamente no SKILL.md/EVIDENCE_POLICY.md.
- Threshold de proteína 1,0–1,3 g/kg/dia como faixa de proteção de massa
  magra em déficit calórico tem respaldo de meta-análise 2024 (Clinical
  Nutrition ESPEN) — bom candidato a virar referência explícita no cálculo
  metabólico.
- Segurança renal de proteína alta em saudáveis (sem DRC) tem meta-análise
  de RCTs recente (22 RCTs) mostrando hiperfiltração adaptativa sem lesão —
  reforça a barreira de segurança já existente.
- Equação de GER: cuidado ao usar Mifflin-St Jeor universalmente — evidência
  recente mostra que ela subestima em atletas; equação pode precisar ser
  parametrizada por população.

## Pendências

- Usuário precisa confirmar se "minha skill" era mesmo nutriplanner-pro.
- Usuário precisa abrir o texto completo dos artigos linkados no arquivo de
  evidências antes de registrar qualquer entrada em `evidence_registry.json`
  (fetch bloqueado neste ambiente, dados vêm de snippet de busca).
- Se quiser, posso desenhar a entrada real no `evidence_registry.json` assim
  que o schema/arquivo estiver disponível neste ambiente (não estava
  sincronizado nesta sessão).
- Decidir se vale trazer nutriplanner-pro para dentro deste repositório
  (`.claude/skills/`) para ter versionamento git e facilitar a geração futura
  de um `AGENTS.md` real a partir dos arquivos completos (scripts,
  knowledge_base) — hoje não foi feito por não ter sido pedido.
