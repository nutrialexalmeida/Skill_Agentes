# Fase 2b — Cálculo metabólico

Entrada: bloco `ANAMNESE`.
Saída: bloco `CALCULO` conforme `contratos/handoff.md`.

## Procedimento

1. Se existir `scripts/calculo_metabolico.py` no repositório da skill,
   execute-o — ele é a fonte autoritativa, com configuração versionada:

   ```
   python scripts/calculo_metabolico.py --refeicoes N
   ```

   Não recalcule à mão por cima do resultado do script. Se o script falhar,
   reporte a falha em `alertas` em vez de improvisar um número.

2. Sem script disponível (Modo App, ou repositório sem os arquivos),
   calcule explicitamente e **mostre a conta**: equação usada, valores
   substituídos, resultado. Um número sem a conta ao lado não é auditável.

## Escolha da equação de GER/TMB

Não use uma equação única para todo mundo. Registre a escolha e o porquê em
`justificativa_da_equacao`:

- **Adulto geral, com ou sem obesidade**: Mifflin-St Jeor é a de melhor
  desempenho médio.
- **Atleta / massa magra elevada**: Mifflin-St Jeor tende a **subestimar**.
  Prefira Cunningham ou Harris-Benedict, e prefira Cunningham quando houver
  massa magra medida.
- **Idoso (≥65 anos) com obesidade**: considere a equação da OMS, que teve
  melhor acurácia nessa população.

Se faltar o dado que a equação preferida exige (ex.: massa magra), use a
alternativa viável e registre a limitação.

## Saída obrigatória

Todos estes, sem exceção:

- GER/TMB, GET e meta energética em kcal.
- Proteína, carboidrato e gordura em **gramas/dia E em g/kg** de peso
  corporal.
- Meta de kcal e dos três macros **por refeição**.

## Distribuição entre as refeições

Modo `padrao` — regra do sistema:

- **Proteína** igual ou próxima em todas as refeições.
- **Gordura** igual ou próxima em todas as refeições.
- **Carboidrato** em pirâmide estritamente decrescente na ordem
  cronológica: a primeira refeição recebe a maior quantidade, cada seguinte
  recebe menos.

A amplitude entre a maior e a menor oferta de proteína ou de gordura não
pode superar a tolerância versionada em `calculos.json`. Sem esse arquivo,
use 15% como tolerância e registre que foi um padrão assumido.

Modos `pre_pos_treino` e `competicao` são as **únicas** exceções à pirâmide
de carboidrato, e exigem percentuais explícitos, justificativa e os nomes
das refeições estratégicas. Competição exige obrigatoriamente as fases
pré-competição, intra-prova e pós-competição. Proteína e gordura continuam
uniformes mesmo nesses modos.

## Guardrails

- Proteína: em restrição calórica, abaixo de 1,0 g/kg/dia há risco
  aumentado de perda de massa magra; a faixa protetora começa em torno de
  1,0–1,3 g/kg/dia. Se a meta ficar abaixo disso, sinalize em `alertas`.
- Meta energética abaixo do guardrail operacional do sistema: não atribua o
  valor ao CFN nem a nenhuma diretriz. Marque
  `meta_abaixo_do_guardrail: true`, exija justificativa e monitoramento do
  nutricionista responsável.

## Base de evidência

A pirâmide de carboidrato decrescente e a faixa protetora de proteína são
escolhas de design com respaldo na literatura recente — se o repositório
tiver `knowledge_base/references/`, cite de lá. Não apresente a regra de
uniformidade de proteína entre refeições como consenso fechado: a evidência
sustenta melhor "quantidade total adequada + pelo menos uma refeição com
dose suficiente" do que uniformidade estrita. A regra permanece como
heurística operacional do sistema, e deve ser apresentada como tal.
