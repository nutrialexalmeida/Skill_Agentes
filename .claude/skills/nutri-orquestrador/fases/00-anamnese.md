# Fase 1 — Anamnese e triagem de segurança

Executada sempre pelo orquestrador, nos dois modos.

## Coletar

Idade, sexo, peso, altura, objetivo, rotina, atividade física, número de
refeições desejado, preferências, restrições, condições clínicas,
medicamentos, exames disponíveis e contexto social.

Pergunte pelos dados **essenciais** ausentes (idade, sexo, peso, altura,
objetivo, número de refeições, restrições, condições clínicas,
medicamentos). Dados opcionais não informados são simplesmente omitidos —
não trave o atendimento por eles.

A ausência de exames recentes, isoladamente, **não bloqueia** um plano para
adulto sem doença renal/hepática, sintomas de alerta ou outra barreira
clínica. Registre a limitação e liste os exames recomendados.

Condição estável e medicamento conhecido exigem **adaptação e
monitoramento**, não a substituição automática do plano por orientações
genéricas.

## Triagem de segurança — barreiras que interrompem a automação

Marque `triagem_seguranca.bloqueado: true` e pare o fluxo se houver:

- **Menor de 18 anos** — não automatize restrição energética sem supervisão
  profissional explicitamente confirmada. Priorize saúde, crescimento,
  hábitos e encaminhamento.
- **Gestação ou lactação**.
- **Transtorno alimentar** suspeito ou diagnosticado.
- **Doença renal ou hepática**.
- **Sintomas de alerta** (perda de peso não intencional, disfagia, dor
  torácica, sangramento, síncope, edema novo, icterícia, etc.).

Bloqueio não é recusa fria: explique o motivo em linguagem acolhida, diga o
que precisa ser avaliado e por quem, e ofereça o que é seguro fazer
enquanto isso (educação alimentar, organização de rotina).

### Sintoma histórico exige adjudicação por escrito

Barreira que aparece no relato **em qualquer tempo verbal** — inclusive como
história passada — precisa ser julgada explicitamente. "Tive disfagia, mas já
faz tempo" não é motivo para bloquear, e também não é motivo para ignorar.

Preencha `triagem_seguranca.motivo` **mesmo quando `bloqueado` for `false`**,
dizendo qual barreira apareceu e por que ela não está ativa. Por exemplo:
`"disfagia relatada como histórica — episódios raros, assintomático há
meses, sem perda de peso involuntária; não bloqueia"`.

`motivo: null` só é válido quando **nenhuma** barreira apareceu no relato.
Silêncio não é adjudicação: para a auditoria, barreira citada sem julgamento
escrito é barreira ignorada, e reprova.

O sinal de que a adjudicação faltou costuma vir das fases seguintes — se a
suplementação bloqueia itens por causa da condição e a prescrição constrói
textura e horário em torno dela, então ela está clinicamente viva e merecia
uma linha aqui.

## Nunca

- Iniciar, suspender ou alterar dose de medicamento.
- Converter "alvo funcional" de exame em diagnóstico.
- Tratar marcador isolado como doença.

## Saída

Bloco `ANAMNESE` conforme `../HANDOFF.md`.

Só marque `dados_essenciais_confirmados: true` quando o usuário tiver de
fato respondido — não presuma valor padrão para peso, altura ou condição
clínica.
