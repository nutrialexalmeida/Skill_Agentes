---
name: roteador
description: Skill inicial do sistema. Deve ser executada no início de TODA solicitação do usuário para (1) analisar o pedido e decidir qual skill/ferramenta deve executá-lo e (2) carregar da memória persistente (memoria/) todo o contexto relevante já discutido em conversas anteriores. Acione sempre que uma nova tarefa, pergunta ou comando chegar.
---

# Roteador — skill inicial do sistema

Você é o ponto de entrada de todas as solicitações. Antes de executar qualquer pedido do usuário, siga estas 4 etapas, nesta ordem.

## Etapa 1 — Analisar o pedido

Identifique:
- **Intenção**: o que o usuário quer que aconteça (criar, corrigir, analisar, publicar, agendar, pesquisar...)
- **Domínio**: código, design (Figma/Canva), redes sociais (Metricool/Meta Ads), e-mail (Gmail), pesquisa (PubMed), GitHub, configuração do sistema, etc.
- **Palavras-chave**: 3 a 6 termos que resumem o assunto (serão usados para buscar na memória)

## Etapa 2 — Carregar contexto da memória (conversas anteriores)

A memória persistente do sistema fica em `memoria/`. Cada conversa relevante grava ali o que foi decidido e produzido, para que outras conversas possam continuar de onde parou.

1. Leia `memoria/INDICE.md` (se o hook já não o injetou na mensagem) para ver os tópicos existentes.
2. Busque as palavras-chave da Etapa 1 nos arquivos de tópico:
   - `Grep` com as palavras-chave em `memoria/topicos/`
3. Leia **apenas** os arquivos de tópico relevantes ao pedido atual (não carregue a memória inteira — economize contexto).
4. Use o conteúdo carregado como contexto de fundo: decisões já tomadas, preferências do usuário, trabalho já feito, pendências.

Se `memoria/` não tiver nada relevante, siga em frente sem contexto extra.

## Etapa 3 — Escolher e executar a skill certa

1. Consulte a lista de skills disponíveis na sessão (listagem de skills do sistema e as skills do projeto em `.claude/skills/`).
2. Regras de decisão:
   - Existe uma skill cujo gatilho/descrição cobre o pedido? → **Invoque-a com a ferramenta Skill** antes de qualquer outra ação.
   - O pedido é um atendimento nutricional que envolve mais de uma etapa (exames, cálculo metabólico, suplementação, montagem de plano)? → Invoque a skill `nutri-orquestrador`, que coordena as fases e despacha para os subagentes `nutri-*`. Não chame os subagentes diretamente: a ordem das fases e a auditoria final são responsabilidade do orquestrador.
   - O pedido envolve um serviço conectado (Figma, Canva, Metricool, Gmail, GitHub, Meta Ads, PubMed...)? → Use `ToolSearch` para carregar as ferramentas MCP adequadas e siga as instruções do servidor (ex.: Figma exige a skill `/figma-use` antes de `use_figma`).
   - Nenhuma skill cobre o pedido? → Execute diretamente com as ferramentas padrão (Read, Edit, Bash, etc.) e registre na memória que não havia skill para esse tipo de pedido (candidata a skill futura).
3. Se o pedido for ambíguo entre duas skills, escolha a mais específica; só pergunte ao usuário se a escolha mudar o resultado de forma significativa.

## Etapa 4 — Atualizar a memória ao final

Depois de concluir o pedido (não antes), grave o que servirá para conversas futuras:

1. Crie ou atualize `memoria/topicos/<slug-do-assunto>.md` no formato:

   ```markdown
   # <Título do assunto>
   Atualizado em: AAAA-MM-DD

   ## Resumo
   O que este assunto é e em que pé está.

   ## Decisões e preferências
   - Decisões tomadas pelo usuário que não devem ser re-perguntadas.

   ## Trabalho realizado
   - AAAA-MM-DD: o que foi feito (arquivos, links, entregas).

   ## Pendências
   - O que ficou para depois.
   ```

2. Atualize a linha correspondente em `memoria/INDICE.md` (uma linha por tópico: `- [slug](topicos/slug.md) — descrição curta — atualizado AAAA-MM-DD`).
3. Grave apenas o que tem valor futuro: decisões, preferências, estado do trabalho, pendências. Não copie conversas inteiras.
4. Se o trabalho estiver em um repositório git e o usuário costuma versionar, faça commit das mudanças de `memoria/` junto com o trabalho.

## O que NÃO fazer

- Não pule a Etapa 2 mesmo em pedidos que parecem simples — o custo é baixo e evita repetir perguntas já respondidas.
- Não carregue todos os arquivos de `memoria/topicos/` — apenas os relevantes.
- Não invente skills: só invoque nomes que aparecem na listagem da sessão.
