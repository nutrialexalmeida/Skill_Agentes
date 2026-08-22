# Modos especiais — as únicas exceções à pirâmide de carboidrato

Leia este arquivo apenas quando `ANAMNESE.modo` for `pre_pos_treino` ou
`competicao`. No modo `padrao` ele é irrelevante.

## Sumário

- [Regra geral das exceções](#regra-geral-das-excecoes)
- [Modo pre_pos_treino](#modo-pre_pos_treino)
- [Modo competicao](#modo-competicao)
- [O que a auditoria confere](#o-que-a-auditoria-confere)

## Regra geral das exceções

A pirâmide de carboidrato estritamente decrescente vale sempre, **exceto**
nestes dois modos formais. Nenhuma outra exceção é permitida — nem
"preferência do paciente", nem "rotina de trabalho", nem "ele treina à
noite" sem que o modo tenha sido formalmente declarado na anamnese.

Em ambos os modos:

- **Proteína e gordura continuam uniformes.** A exceção libera apenas o
  carboidrato. Isso não é negociável em nenhum modo.
- A exceção precisa de **percentuais explícitos** de como o carboidrato foi
  redistribuído.
- A exceção precisa de **justificativa escrita** ligada ao objetivo do
  paciente.
- As **refeições estratégicas precisam ser nomeadas** — não basta dizer que
  há uma exceção, é preciso dizer em quais refeições ela acontece.

Faltando qualquer um dos três, o modo não está formalmente declarado e o
plano volta para o modo `padrao`.

## Modo pre_pos_treino

Redistribui carboidrato em torno da sessão de treino.

Registre em `PRESCRICAO`:

- Horário do treino e horário de cada refeição estratégica.
- Percentual do carboidrato diário alocado na refeição pré-treino e na
  pós-treino.
- Justificativa: o que essa alocação pretende sustentar (desempenho na
  sessão, reposição de glicogênio, tolerância gastrointestinal).

Fora das refeições estratégicas, a pirâmide decrescente continua valendo
entre as refeições restantes, na ordem cronológica delas.

## Modo competicao

O mais restrito dos três. Exige **obrigatoriamente as três fases** — plano
sem alguma delas é reprovado:

1. **Pré-competição** — carga e horário da última refeição antes da prova,
   com atenção ao tempo de esvaziamento gástrico.
2. **Intra-prova** — o que é consumido durante, em que intervalo, com
   quantidade em gramas e volume de líquido.
3. **Pós-competição** — janela de reposição, com carboidrato e proteína
   quantificados.

Registre também:

- Modalidade, duração prevista e horário de largada.
- Se o protocolo já foi testado em treino. Protocolo nunca testado em
  treino não vai para o dia da prova: registre isso como alerta explícito,
  em vez de entregá-lo como se fosse seguro.

## O que a auditoria confere

O validador automático (`../scripts/validar_plano.py`) **não reprova** a quebra
da pirâmide quando o modo é especial — ele apenas conta as quebras e
devolve para julgamento. Quem confere a justificativa, os percentuais, os
nomes das refeições estratégicas e a presença das três fases de competição é
o auditor, lendo este arquivo.

Ou seja: nestes modos a auditoria automática é mais frouxa e a humana precisa
ser mais atenta. Não confunda "o script passou" com "o modo especial está
correto".
