# Sistema roteador e memória persistente

Atualizado em: 2026-07-12

## Resumo

O repositório `Agentes` usa uma skill inicial chamada `roteador` que roda em toda mensagem do usuário. Ela decide qual skill/ferramenta executa o pedido e carrega desta pasta (`memoria/`) o contexto de conversas anteriores.

## Decisões e preferências

- O usuário se comunica em português; respostas e arquivos do sistema em português.
- Toda mensagem do usuário passa pelo roteador (garantido por hook `UserPromptSubmit` em `.claude/settings.json`).
- Contexto entre conversas é compartilhado via arquivos em `memoria/topicos/`, indexados em `memoria/INDICE.md` — sessões não enxergam o histórico umas das outras diretamente.
- Ao final de cada tarefa relevante, a conversa deve gravar aqui decisões, trabalho feito e pendências.

## Trabalho realizado

- 2026-07-12: criado o sistema — skill `roteador`, hook de injeção por mensagem, estrutura de memória e CLAUDE.md.

## Pendências

- Criar skills específicas por domínio (ex.: redes sociais, design, e-mail) conforme surgirem tarefas recorrentes.
