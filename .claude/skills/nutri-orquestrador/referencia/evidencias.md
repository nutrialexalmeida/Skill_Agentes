# Base de evidência das regras do sistema

Leia este arquivo quando questionarem **por que** uma regra existe, ou ao
decidir a força com que apresentar uma recomendação. Não é necessário para
executar as fases.

## Sumário

- [Como usar esta base](#como-usar-esta-base)
- [Escolha da equação de GER](#escolha-da-equacao-de-ger)
- [Faixa protetora de proteína](#faixa-protetora-de-proteina)
- [Pirâmide de carboidrato decrescente](#piramide-de-carboidrato-decrescente)
- [Uniformidade de proteína entre refeições](#uniformidade-de-proteina-entre-refeicoes)
- [Segurança renal de dieta hiperproteica](#seguranca-renal-de-dieta-hiperproteica)
- [Status de verificação](#status-de-verificacao)

## Como usar esta base

Três níveis de confiança, e a linguagem muda conforme o nível:

- **Sustentado por meta-análise recente com amostra grande** → pode ser
  apresentado como recomendação.
- **Sustentado por revisão com achados mistos** → apresente como conduta
  preferida do sistema, dizendo que a evidência é mista.
- **Heurística operacional do sistema** → apresente como escolha de design,
  nunca como consenso científico.

Se o repositório tiver `knowledge_base/references/evidence_registry.json`,
a classificação individual de cada item vale mais que este resumo.

## Escolha da equação de GER

**Nível: sustentado.** Não existe equação única boa para toda população.

| População | Equação preferida | Observação |
|---|---|---|
| Adulto geral, com ou sem obesidade | Mifflin-St Jeor | melhor desempenho médio |
| Atleta / massa magra elevada | Cunningham ou Harris-Benedict | Mifflin-St Jeor **subestima** |
| Idoso ≥65 anos com obesidade | OMS | melhor acurácia nessa faixa |

Base: revisão sistemática com meta-análise em atletas (29 estudos, 1.430
participantes, ~100 equações avaliadas) mostrando subestimação do
Mifflin-St Jeor; e estudo de validação em idosos com obesidade, com OMS em
59,0% de acurácia contra 53,5% do Harris-Benedict.

## Faixa protetora de proteína

**Nível: sustentado.** Em restrição calórica, abaixo de 1,0 g/kg/dia há
risco aumentado de perda de massa magra; acima de 1,3 g/kg/dia a tendência
é de ganho. A faixa protetora usada pelo sistema começa em 1,0–1,3 g/kg/dia.

Base: meta-análise de RCTs em adultos com sobrepeso/obesidade (Clinical
Nutrition ESPEN, 2024) e network meta-analysis de 83 RCTs (International
Journal of Obesity, 2025) mostrando redução de massa corporal, IMC,
circunferência de cintura e massa gorda com dieta hiperproteica.

## Pirâmide de carboidrato decrescente

**Nível: sustentado.** Concentrar a energia — e o carboidrato — mais cedo no
dia associa-se a maior perda de peso e a menores excursões glicêmicas
pós-prandiais.

Base: meta-análise de 29 RCTs com 2.485 adultos (JAMA Network Open, 2024):
distribuição calórica mais cedo no dia −1,75 kg; menor frequência de
refeições −1,85 kg; jejum por horário −1,37 kg, todos contra controle e com
duração mínima de 12 semanas.

Esta é a evidência mais forte por trás de uma regra estrutural do sistema —
cite-a quando questionarem a pirâmide.

## Uniformidade de proteína entre refeições

**Nível: heurística operacional.** Apresente como escolha de design do
sistema, **não** como consenso científico.

A literatura de 2024 sustenta melhor "quantidade total adequada + pelo menos
uma refeição com dose suficiente para estimular a síntese proteica" do que
uniformidade estrita entre refeições. Para adultos já consumindo
0,8–1,3 g/kg/dia, a evidência de uma distribuição "ótima" é limitada e
inconsistente, e o efeito da distribuição não se separa bem do efeito da
quantidade total.

Base: revisão em Frontiers in Nutrition (2024) e o debate publicado no
International Journal of Sport Nutrition and Exercise Metabolism 34(5), 2024.

A regra permanece no sistema porque simplifica a montagem e a adesão, e
porque garante por construção que nenhuma refeição fique com dose
insuficiente. Mas se um nutricionista discordar dela, ele tem respaldo na
literatura — não trate a discordância como erro.

## Segurança renal de dieta hiperproteica

**Nível: sustentado, com ressalva de prazo.** Em adultos **sem** doença
renal crônica, dieta hiperproteica eleva a taxa de filtração glomerular sem
evidência bioquímica consistente de lesão — hiperfiltração adaptativa e
reversível, não dano.

Base: revisão sistemática com meta-análise de 22 RCTs comparando dietas de
~25–35% da energia ou ≥2,0 g/kg/dia contra proteína normal; creatinina
sérica sem mudança significativa.

Ressalva: os estudos são majoritariamente de curto prazo e refletem
adaptação hemodinâmica. Isso **não** flexibiliza a barreira de segurança —
doença renal ou hepática continua suspendendo a automação.

## Status de verificação

Os dados acima vieram de resumos e abstracts indexados em busca, não de
leitura de texto completo (o ambiente onde foram levantados bloqueava o
acesso aos PDFs). Antes de registrar qualquer um deles em
`knowledge_base/references/evidence_registry.json` como referência formal,
abra o artigo e confirme desenho, N e tamanho de efeito.

Ao citar para um profissional, seja honesto sobre isso: diga que o número
vem do resumo, se for o caso. Nunca apresente um N ou um tamanho de efeito
que você não viu no texto completo.
