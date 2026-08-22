# Fase 3a — Suplementação e fitoterapia

Entrada: blocos `ANAMNESE`, `EXAMES`, `CALCULO`.
Saída: bloco `SUPLEMENTACAO` conforme `../HANDOFF.md`.

## Política: bloquear por padrão

O default é **não liberar**. Liberação é exceção justificada, não o
resultado esperado desta fase. Item ausente da base, desatualizado ou sem
validação profissional **não é liberado** — sem discussão.

Nunca libere um suplemento apenas porque ele aparece na base de dados.
Aparecer na base significa que ele foi catalogado, não que está indicado
para este paciente.

## Procedimento

1. Se existir `scripts/regulatory_gate.py`, execute-o para cada item. O
   resultado do gate é vinculante: gate bloqueou, o item está bloqueado.
   Você não tem autoridade para reverter.

   ```
   python scripts/regulatory_gate.py
   ```

2. Sem o script disponível, aplique o gate manualmente e diga
   explicitamente no `observacoes` que o gate automatizado não estava
   disponível e que a liberação depende de conferência do nutricionista
   responsável.

3. Para cada item avaliado, registre nível de evidência e fonte. Nível C/D
   é hipótese ou inspiração prática — nunca justificativa suficiente para
   liberar.

4. Todo item liberado sai com
   `aprovacao_profissional_necessaria: true`. Esta fase propõe; quem
   prescreve é o nutricionista responsável.

## Fitoterapia

Além de tudo acima: confirme se a prescrição exige habilitação específica.
Sem confirmação de habilitação, bloqueie.

## Interações

Cruze cada item com `medicamentos` e `condicoes_clinicas` da anamnese e com
os achados de `EXAMES`. Interação plausível → bloqueie e registre o motivo,
mesmo que o gate regulatório tenha liberado. O gate cobre regulação, não
interação individual.

## Pesquisa de evidência

Se precisar buscar literatura e houver ferramenta de busca disponível,
priorize revisões sistemáticas e meta-análises recentes com amostra
suficiente. Registre em `fonte` o que você de fato leu — se leu apenas o
resumo/abstract, diga isso. Nunca cite N de participantes ou tamanho de
efeito que você não viu no texto.

## Nunca

- Iniciar, suspender ou alterar dose de medicamento.
- Sugerir suplemento como substituto de avaliação médica de um achado
  laboratorial alterado.
- Prometer efeito clínico que a evidência não sustenta.
