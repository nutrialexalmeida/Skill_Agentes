# Fase 3b — Prescrição do plano alimentar

Entrada: blocos `ANAMNESE`, `EXAMES`, `CALCULO`.
Saída: bloco `PRESCRICAO` conforme `contratos/handoff.md`.

Você monta o cardápio real que cumpre as metas que a fase de cálculo
definiu. Você **não redefine as metas** — se elas parecem erradas, registre
em `alertas` e devolva; não conserte por conta própria.

## Base de alimentos

1. Resolva todo alimento primeiro pela **TACO**, em
   `knowledge_base/tables/alimentos.json`.
2. A **TBCA 7.3** serve somente para conferência externa, conforme
   `knowledge_base/tables/TBCA_POLICY.md`. Não copie valores dela para o
   repositório.
3. Nunca some ou complete nutriente ausente com outra base sem registrar
   uma entrada nova completa: fonte, versão, alimento e estado de preparo.
4. Alimento que não está na base não entra no plano. Sem exceção, sem
   estimativa "de cabeça".

## Como escrever cada item

Para cada alimento: nome, medida caseira/porção e **quantidade exata em
gramas**.

- Sem medida caseira validada → escreva "porção de X g". Nunca invente
  equivalência.
- Proibido "livre", "à vontade" ou medida sem equivalência quando o item
  contribui para a meta. Item de contribuição desprezível (tempero, ervas)
  pode ser listado à parte como livre, e explicitamente marcado assim.
- Refeições em ordem cronológica de consumo, com horário sugerido.

## Distribuição — a regra inegociável do modo padrão

- Proteína igual ou próxima em todas as refeições.
- Gordura igual ou próxima em todas as refeições.
- Carboidrato em pirâmide **estritamente decrescente**: cada refeição recebe
  menos que a anterior.

Amplitude máxima entre a maior e a menor oferta de proteína/gordura: a
tolerância de `calculos.json` (padrão assumido 15% se o arquivo não
existir).

Exceção só nos modos `pre_pos_treino` ou `competicao`, declarados na
anamnese, com percentuais explícitos, justificativa e nomes das refeições
estratégicas. Competição exige as fases pré, intra e pós. Proteína e gordura
seguem uniformes mesmo nesses modos.

## Convergência

1. Se existir `scripts/meal_engine.py`, execute-o:

   ```
   python scripts/meal_engine.py
   ```

2. Ajuste alimentos e porções e **repita** até o cardápio real passar em:
   metas diárias, uniformidade de proteína e gordura, e pirâmide de
   carboidrato (ou uma exceção formalmente declarada).

3. Alvos de convergência:
   - Calorias reais dentro de **±2%** da meta.
   - Proteína, carboidrato e gordura reais dentro de **±5%** das metas.

4. Não entregue um cardápio que não convergiu dizendo que "está próximo".
   Se depois de várias iterações não convergir, registre em `alertas` o
   que travou (ex.: restrição alimentar incompatível com a meta de
   proteína) e devolva ao orquestrador.

## Substituições

- Pelo menos **uma troca prática por componente principal** de cada
  refeição.
- Gere somente com `scripts/substitution_engine.py` quando ele existir.
  Sem o script, calcule a equivalência pela mesma base TACO e registre em
  `observacoes` que o motor não estava disponível.
- Exiba alimento original e substituto, cada um com medida caseira/porção e
  gramas.
- Não use porção fixa de guia impresso quando ela divergir da base
  nutricional. A base manda.

## Exibir sempre

kcal, proteína, carboidrato e gordura **planejados e reais por refeição**, e
os totais do dia. Sem isso a auditoria não tem o que conferir.
