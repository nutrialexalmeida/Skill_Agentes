# Avaliações da skill

Três cenários que cobrem as lacunas que motivaram esta skill. Cada um testa
um caminho diferente do fluxo:

| Eval | Testa | Falha típica sem a skill |
|---|---|---|
| `01-adulto-saudavel.json` | caminho feliz completo | entrega "pré-plano" e para; macros só em g/dia, sem g/kg; não audita |
| `02-barreira-seguranca.json` | interrupção por triagem | monta o cardápio de déficit para a adolescente mesmo assim |
| `03-modo-competicao.json` | exceção formal + fases obrigatórias | quebra a pirâmide sem declarar modo; esquece a fase intra-prova |

## Por que estes três

Foram escritos a partir das falhas reais que o sistema pretende evitar, não
de requisitos imaginados:

- **01** existe porque o comportamento sem skill costuma parar em
  recomendações genéricas em vez de entregar um plano auditado.
- **02** existe porque a barreira de segurança é a regra mais importante e a
  mais fácil de contornar sob pressão de um pedido direto e simpático.
- **03** existe porque o modo especial é o único ponto onde uma regra
  estrutural pode ser quebrada legitimamente — e onde a auditoria automática
  é mais frouxa, então o julgamento precisa ser mais firme.

## Como rodar

Não há executor automático neste repositório. Rode manualmente:

1. Abra uma sessão limpa (sem o contexto desta conversa).
2. Cole o `query` do eval.
3. Confira a resposta contra cada item de `expected_behavior`.
4. Anote quais falharam.

Teste com **Haiku, Sonnet e Opus**. Instrução que só funciona no modelo mais
forte é instrução mal escrita — o eval 02 em particular deve passar em
todos, porque é o de segurança.

Rode também nos **dois modos**: Claude Code (com subagentes) e app claude.ai
(sequencial). O resultado clínico deve ser equivalente; se divergir, a causa
provável é regra duplicada fora de `fases/`.

## Ao mudar uma regra

Se a mudança toca cálculo, distribuição ou auditoria, rode os três evals
antes do commit. Se a mudança cria um comportamento que nenhum eval cobre,
escreva um quarto.

## fixtures/

Arquivos de apoio para evals que precisem de anexo (exames em PDF, planilha
de plano existente). Use apenas dados fictícios ou anonimizados — este
repositório é versionado.
