# Agentes — sistema de skills com roteador e memória persistente

Comandos para Agentes de IA. Este repositório funciona como um "sistema operacional" de skills: toda solicitação do usuário passa primeiro pela skill inicial `roteador`.

## Regra principal

Antes de executar qualquer pedido do usuário, siga a skill `roteador` (`.claude/skills/roteador/SKILL.md`):

1. Analise o pedido (intenção, domínio, palavras-chave).
2. Carregue da memória persistente (`memoria/`) os tópicos relevantes de conversas anteriores.
3. Escolha a skill/ferramenta adequada e execute.
4. Ao concluir, atualize `memoria/topicos/` e `memoria/INDICE.md`.

Um hook `UserPromptSubmit` (`.claude/settings.json` → `.claude/hooks/roteador-contexto.sh`) reforça essa regra injetando a instrução e o índice da memória em toda mensagem.

## Estrutura

- `.claude/skills/` — skills do sistema (a `roteador` é a inicial; crie novas skills por domínio aqui).
- `.claude/agents/` — subagentes especializados, acionados por uma skill orquestradora (não diretamente pelo usuário).
- `.claude/hooks/roteador-contexto.sh` — hook que injeta roteamento + índice da memória por mensagem.

## Orquestração multiagente (nutrição)

A skill `nutri-orquestrador` coordena um atendimento nutricional completo em
fases. As regras clínicas moram em `.claude/skills/nutri-orquestrador/fases/`
— fonte única de verdade, lida tanto pelos subagentes (Claude Code) quanto
pelo próprio orquestrador (app claude.ai, sem subagentes).

Fluxo: anamnese → (exames ‖ cálculo) → (suplementação ‖ prescrição) →
auditoria independente. O auditor é sempre uma instância nova que não
participou da montagem.

Ao mexer numa regra clínica, edite o arquivo de fase — nunca duplique a
regra dentro do arquivo de agente, que é só um invólucro fino.
- `memoria/INDICE.md` — índice dos tópicos da memória (uma linha por tópico).
- `memoria/topicos/*.md` — um arquivo por assunto: resumo, decisões, trabalho realizado, pendências.

## Memória persistente

- Sessões/conversas não compartilham histórico entre si; `memoria/` é a ponte.
- Grave apenas o que tem valor futuro (decisões, preferências, estado, pendências) — nunca conversas inteiras.
- Commit das mudanças de `memoria/` junto com o trabalho, para que outras conversas vejam.

## Idioma

Responda e escreva arquivos do sistema em português (pt-BR).
