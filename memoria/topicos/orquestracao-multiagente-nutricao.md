# Orquestração multiagente para atendimento nutricional

Atualizado em: 2026-08-22

## Resumo

Criado no repositório `Skill_Agentes` um sistema de orquestração em fases
para atendimento nutricional completo: uma skill orquestradora
(`nutri-orquestrador`) coordena cinco etapas especializadas e uma auditoria
final independente. Funciona no Claude Code (com subagentes reais, em
paralelo) e no app claude.ai (mesmas fases, sequenciais).

## Decisões e preferências

- **Skill não despacha para skill.** Skill só carrega instrução no mesmo
  contexto. Quem despacha trabalho para contexto isolado é o Agent tool
  (`.claude/agents/*.md`). O usuário aceitou esse mapeamento.
- **Fonte única de verdade em `fases/`.** As regras clínicas moram só em
  `.claude/skills/nutri-orquestrador/fases/`. Os arquivos de agente são
  invólucros finos que mandam ler a fase. Isso evita divergência entre a
  versão Code e a versão App. Ao mudar regra, editar a fase — nunca duplicar
  dentro do agente.
- **Dual-mode obrigatório.** O usuário quer que funcione nos dois ambientes,
  com potencial máximo no Claude Code. A SKILL.md tem uma Fase 0 que detecta
  o modo (existe ferramenta Agent + `.claude/agents/nutri-*.md`?) e anuncia
  ao usuário em qual modo está.
- **Auditor sempre instância nova.** Em Modo Code o auditor é um subagente
  que não participou da montagem — o isolamento é o que torna a auditoria
  confiável. O auditor não tem `Write`/`Edit` no `tools:`, então não
  consegue consertar o plano, só reprovar e apontar a fase responsável.
- **Máximo 2 ciclos de correção.** Na terceira auditoria com falha, entrega
  o que passou e o que não passou, explicitamente. Nunca entregar reprovado
  como aprovado.
- **Degradação graciosa.** Se scripts/knowledge_base do nutriplanner-pro não
  existirem, cada fase cai para modo manual, mostra a conta por extenso e
  registra a limitação. Tolerância de uniformidade assume 15% como padrão
  declarado quando `calculos.json` não existe.

## Arquitetura implementada

Fluxo: anamnese → (exames ‖ cálculo) → (suplementação ‖ prescrição) →
auditoria → reciclagem ou entrega.

Ondas paralelas definidas por dependência: exames e cálculo só dependem da
anamnese; suplementação e prescrição consomem anamnese+exames+cálculo.

Arquivos criados:
- `.claude/skills/nutri-orquestrador/SKILL.md` — orquestrador dual-mode
- `.claude/skills/nutri-orquestrador/README.md` — como empacotar nos dois ambientes
- `.claude/skills/nutri-orquestrador/contratos/handoff.md` — schemas JSON
  dos blocos ANAMNESE, EXAMES, CALCULO, SUPLEMENTACAO, PRESCRICAO, AUDITORIA
- `.claude/skills/nutri-orquestrador/fases/00-anamnese.md` até `05-auditoria.md`
- `.claude/agents/nutri-{exames,calculo,suplementacao,prescricao,auditor}.md`

Regras clínicas migradas do `SKILL.md` original da nutriplanner-pro
(TACO/TBCA, pirâmide de carboidrato, uniformidade proteína/gordura, gate
regulatório bloqueia por padrão, barreiras de segurança, tolerâncias ±2%
kcal e ±5% macros). Incorporados também os achados de evidência 2024-2026
levantados na sessão anterior: escolha de equação de GER por população
(Mifflin-St Jeor subestima em atleta; OMS melhor em idoso obeso), faixa
protetora de proteína 1,0–1,3 g/kg em déficit, e a ressalva de que
uniformidade estrita de proteína entre refeições é heurística operacional,
não consenso fechado.

## Trabalho realizado

- 2026-08-22: implementada a arquitetura completa (13 arquivos), ligada ao
  `roteador` (regra de decisão nova: atendimento multi-etapa → invocar
  `nutri-orquestrador`, nunca chamar subagente direto) e documentada no
  `CLAUDE.md`. Branch `claude/skill-review-improvements-fxhipo`.

## Reorganização em pacote modular (2026-08-22, segunda rodada)

Reestruturado seguindo as práticas oficiais de autoria de skills, em três
camadas por **frequência de uso** (não por importância):

- `fases/` — lido em todo atendimento.
- `referencia/` — lido só quando a condição aparece: `modos-especiais.md`
  (modo != padrao), `evidencias.md` (questionaram o porquê),
  `troubleshooting.md` (algo travou), `incorporar-material.md` (processar
  entrada/).
- `scripts/validar_plano.py` — executado, não lido.

Decisões desta rodada:

- **Critério de divisão**: conteúdo sempre necessário fica na fase; só vai
  para `referencia/` o que é genuinamente condicional. Evitou-se mover a
  tabela de equações de GER (sempre necessária) — só a justificativa de
  evidência dela saiu.
- `contratos/handoff.md` virou `HANDOFF.md` na raiz (pasta com um arquivo só
  era estrutura vazia). `README.md` virou `MANUTENCAO.md` (é doc de
  mantenedor, não de execução).
- **Validador determinístico** criado e testado: confere somas por refeição,
  totais do dia, tolerâncias ±2%/±5%, uniformidade P/G, pirâmide de
  carboidrato par a par e gramas explícitas. Códigos de saída 0/1/2.
  Tolerâncias vêm de `calculos.json` quando existe; senão usa padrões
  declarados no próprio script, e informa a origem na saída. Em modo
  especial ele **não** reprova a quebra da pirâmide — só conta e devolve
  para julgamento humano.
- Ciclo de feedback: a fase de prescrição roda o mesmo validador antes de
  devolver, para não queimar ciclo de auditoria.
- **Três evals** criados (`evals/`): adulto saudável (caminho feliz),
  barreira de segurança (adolescente com pedido de déficit agressivo — testa
  a interrupção), modo competição (exceção formal + três fases
  obrigatórias). Sem executor automático: rodar manualmente, em sessão
  limpa, nos três modelos e nos dois modos.
- **Pasta `entrada/`** criada na raiz do repositório (não dentro da skill,
  para não poluir o pacote que sobe ao claude.ai). Usuário solta material
  novo lá e pede "processa a entrada". Fluxo em
  `referencia/incorporar-material.md`: classificar → questionar origem,
  conflito, força de evidência e impacto em segurança → propor destino →
  **aguardar confirmação antes de mudar regra clínica** → aplicar →
  arquivar em `entrada/processados/AAAA-MM/`.
- Caminhos relativos normalizados: arquivo em subpasta usa `../` para
  referenciar irmãos de outra pasta.

Tamanhos: SKILL.md 135 linhas, maior arquivo de fase 125, validador 385.
Todos bem abaixo do limite de 500.

## Ressalva sobre "alta liberdade"

O guia pedia "alta liberdade (instruções baseadas em texto)". Aplicado
**diferencialmente**, não de forma uniforme — o próprio princípio diz para
ajustar à fragilidade da tarefa:

- Alta liberdade: conversa de anamnese, escolha de alimentos, redação da
  entrega.
- Baixa liberdade (especificação apertada): barreiras de segurança,
  tolerâncias numéricas, gate regulatório, checklist de auditoria. São
  tarefas frágeis, de baixa variabilidade e alto custo de erro.

## Pendências

- **Não testado end-to-end.** Os três evals foram escritos mas nunca
  executados. O validador Python foi testado (caso conforme, caso com 9
  defeitos plantados, entrada malformada — todos com o resultado esperado),
  mas o fluxo completo do atendimento não. Rodar `evals/` em sessão limpa,
  nos três modelos e nos dois modos, antes de usar em atendimento real.
- Os scripts e o `knowledge_base/` da nutriplanner-pro não estão neste
  repositório — as fases os referenciam mas caem em modo manual. Decidir se
  vale trazer a nutriplanner-pro para cá e unificar.
- Verificar se a versão App realmente carrega os arquivos de `fases/` como
  esperado depois de subir a pasta como Skill pessoal no claude.ai.
- Considerar um agente de pesquisa científica separado (hoje a pesquisa de
  evidência está embutida na fase de suplementação).
