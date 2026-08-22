# Fase 2a — Análise de exames laboratoriais (finalidade nutricional)

Entrada: bloco `ANAMNESE` + exames fornecidos.
Saída: bloco `EXAMES` conforme `contratos/handoff.md`.

## O que esta fase faz

Traduz marcadores laboratoriais em **implicações para o plano alimentar**.
Nada além disso.

## O que esta fase NÃO faz

- Não diagnostica doença. Marcador alterado é achado, não diagnóstico.
- Não trata marcador isolado como doença — cruze com clínica, uso de
  medicamento e contexto antes de sugerir qualquer implicação.
- Não converte "alvo funcional" ou "faixa ótima" de literatura de nicho em
  meta clínica. Use faixas laboratoriais e diretrizes reconhecidas; se citar
  uma faixa mais estreita, diga explicitamente que é preferência de conduta,
  não referência oficial.
- Não altera, inicia ou suspende medicamento.

## Procedimento

1. Se não houver exames: devolva `disponivel: false`, preencha
   `exames_recomendados` com o que faria diferença para este objetivo
   específico (não uma lista genérica), e siga. Isso não bloqueia o plano
   de um adulto sem barreira clínica.
2. Para cada marcador informado: registre valor, unidade, faixa de
   referência do laboratório (se veio junto) e situação.
3. Para cada marcador **fora** da faixa, avalie se há implicação nutricional
   real. Muitos não têm — nesse caso registre `relevancia_nutricional:
   "sem implicação direta para o plano"` em vez de forçar uma conduta.
4. Se algum achado sugerir barreira de segurança que a anamnese não pegou
   (ex.: função renal ou hepática alterada), registre em `alertas` com
   destaque. O orquestrador vai reavaliar a triagem.

## Cuidado com contexto

- Medicamento em uso pode explicar o marcador. Registre a hipótese.
- Exame antigo tem valor limitado. Registre a data e sinalize se estiver
  desatualizado para a decisão em questão.
- Variação intraindividual e condições de coleta (jejum, exercício recente,
  hidratação) afetam vários marcadores. Não trate um valor limítrofe único
  como tendência.

## Base de evidência

Se o repositório da skill tiver `knowledge_base/references/EVIDENCE_POLICY.md`
e `knowledge_base/references/evidence_registry.json`, leia-os e respeite a
classificação: material nível C/D é hipótese ou inspiração prática, nunca
justificativa suficiente para uma conduta.
