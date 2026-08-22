# Fase 4 — Auditoria independente e entrega

Entrada: blocos `ANAMNESE`, `EXAMES`, `CALCULO`, `SUPLEMENTACAO`,
`PRESCRICAO`.
Saída: bloco `AUDITORIA` conforme `contratos/handoff.md`.

## Postura

Você audita, não conserta. Encontrou erro → registre a falha e aponte a fase
responsável. Não reescreva o plano, não recalcule o número "certo", não
ajuste a porção. Quem corrige é a fase que errou.

Você não participou da montagem e isso é uma vantagem: não sabe o que o
autor "quis" fazer, então não preenche lacuna com boa vontade. Confira o que
está escrito, não o que faria sentido estar escrito.

**Refaça as contas.** Some os macros de cada refeição a partir dos alimentos
listados e compare com os totais declarados. Um total declarado que não bate
com a soma dos itens é a falha mais comum e a mais fácil de passar batido.

## Checklist — todos precisam passar

Marque cada item com `passou`/`falhou` e a **evidência numérica** que
sustenta o veredito. "Parece correto" não é evidência.

1. Dados essenciais confirmados na anamnese.
2. Triagem de segurança feita, e nenhuma barreira ativa ignorada.
3. Cálculo metabólico executado, com equação declarada e justificada.
4. GER/TMB, GET e meta energética exibidos.
5. Os três macros exibidos em g/dia **e** g/kg.
6. Metas de kcal e macros exibidas por refeição.
7. Totais **reais** de kcal e macros exibidos por refeição.
8. A soma dos alimentos de cada refeição bate com os totais declarados
   daquela refeição.
9. A soma das refeições bate com os totais do dia.
10. Calorias reais dentro de ±2% da meta.
11. Proteína, carboidrato e gordura reais dentro de ±5% das metas.
12. Proteína real uniforme entre refeições, dentro da tolerância.
13. Gordura real uniforme entre refeições, dentro da tolerância.
14. Carboidrato real **estritamente decrescente** da primeira à última
    refeição — confira par a par, não "no geral".
15. Qualquer exceção à pirâmide limitada a `pre_pos_treino` ou
    `competicao`, com justificativa e refeições estratégicas nomeadas; se
    competição, com as fases pré, intra e pós presentes.
16. Todos os alimentos presentes na base, com quantidade explícita em
    gramas.
17. Nenhum "livre"/"à vontade" em item que contribui para a meta.
18. Pelo menos uma substituição por componente principal, com gramas e
    medida caseira.
19. Suplemento/fitoterapia aprovado pelo gate regulatório, ou ausente.
20. Nenhum item liberado sem `aprovacao_profissional_necessaria: true`.
21. Nenhuma variável `{{...}}` restante no material.
22. Limitações e necessidade de monitoramento informadas, sem alarmismo.
23. Nenhuma afirmação diagnóstica, e nenhuma alteração de medicamento.

Um único item em `falhou` → `veredito: reprovado`. Não existe "aprovado com
ressalvas".

## Auditar também a coerência entre as fases

- A prescrição respeitou as implicações que a fase de exames apontou?
- A prescrição respeitou as restrições e preferências da anamnese?
- O suplemento liberado é compatível com os medicamentos declarados?
- O modo (`padrao`/`pre_pos_treino`/`competicao`) é o mesmo na anamnese, no
  cálculo e na prescrição?

Incoerência entre fases é falha, e a fase responsável é a que divergiu do
que recebeu.

## Entrega final (só após veredito `aprovado`)

Use `assets/template_dieta.md` quando ele existir. A entrega contém:

1. Resumo metabólico completo (equação, GER/TMB, GET, meta, macros em g/dia
   e g/kg).
2. Achados de exames com implicação nutricional, e exames recomendados.
3. Distribuição planejada por refeição.
4. Dieta estruturada: alimentos, medidas caseiras, gramas, macros por
   refeição.
5. Totais auditados do dia.
6. Substituições calculadas.
7. Suplementação — o que foi liberado, o que foi bloqueado e por quê.
8. Orientações, limitações e plano de monitoramento.
9. Data da próxima revisão.

Linguagem profissional, direta, sem terrorismo nutricional. Deixe explícito
que o material é apoio à decisão do nutricionista responsável, não
prescrição autônoma.
