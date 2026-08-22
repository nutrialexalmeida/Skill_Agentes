# Quando uma fase falha ou não converge

Leia quando algo travar. Não é necessário no caminho feliz.

## Sumário

- [O cardápio não converge nas tolerâncias](#o-cardapio-nao-converge-nas-tolerancias)
- [Não dá para manter proteína uniforme](#nao-da-para-manter-proteina-uniforme)
- [A pirâmide de carboidrato não fecha](#a-piramide-de-carboidrato-nao-fecha)
- [Um script não existe ou falhou](#um-script-nao-existe-ou-falhou)
- [Alimento não está na base](#alimento-nao-esta-na-base)
- [A auditoria reprova em ciclo](#a-auditoria-reprova-em-ciclo)
- [Um subagente devolveu algo incompleto](#um-subagente-devolveu-algo-incompleto)
- [Um subagente morreu no meio da fase](#um-subagente-morreu-no-meio-da-fase)

## O cardápio não converge nas tolerâncias

±2% em kcal e ±5% nos macros. Se depois de várias iterações não fecha, a
causa quase sempre é uma destas:

1. **Poucos alimentos com pouca variedade de macros.** Um cardápio só com
   fontes mistas não permite ajustar um macro sem mexer nos outros.
   Introduza uma fonte mais isolada (proteína magra, óleo, carboidrato de
   baixa gordura) para ganhar um grau de liberdade.
2. **Meta incompatível com as restrições.** Meta de 2,2 g/kg de proteína com
   restrição a lácteos, ovos e carne vermelha pode simplesmente não fechar.
3. **Número de refeições alto demais para a meta energética.** Seis refeições
   em 1.400 kcal deixa cada refeição pequena demais para acomodar a
   uniformidade de proteína.

Não force o encaixe arredondando porções para números irreais (37,5 g de
frango em três refeições). Registre em `alertas` o que travou e devolva ao
orquestrador — a fase de cálculo pode precisar rever a meta ou o número de
refeições com o usuário.

## Não dá para manter proteína uniforme

Verifique primeiro se o problema é a **primeira ou a última** refeição —
costuma ser. Café da manhã com pouca proteína e jantar com muita é o padrão
cultural que mais briga com esta regra.

Se a restrição for real e não contornável, a saída é rever o número de
refeições com o usuário, não quebrar a regra em silêncio.

## A pirâmide de carboidrato não fecha

Confira se a **ordem cronológica** está correta em `ordem`. A pirâmide é
avaliada na ordem em que as refeições são consumidas, não na ordem em que
foram escritas no JSON.

Se a ordem está certa e ainda assim não fecha, a última refeição
provavelmente ficou com carboidrato demais para acomodar as calorias. Tire
carboidrato do fim e compense com gordura, que é uniforme e não entra na
pirâmide.

Se o caso genuinamente exige carboidrato à noite (treino noturno,
competição), isso é um **modo especial** e precisa ser declarado
formalmente na anamnese — ver `modos-especiais.md`. Não quebre a
pirâmide sem declarar o modo.

## Um script não existe ou falhou

Os scripts do NutriPlanner (`calculo_metabolico.py`, `meal_engine.py`,
`substitution_engine.py`, `regulatory_gate.py`) podem não estar presentes,
dependendo de onde a skill está instalada.

- **Ausente** → caia para o modo manual, mostre a conta por extenso e
  registre em `observacoes` que o motor não estava disponível.
- **Falhou na execução** → reporte a falha em `alertas` com a mensagem de
  erro. Não improvise um número para substituir o que o script devolveria.

Exceção que não admite fallback: `regulatory_gate.py` ausente **não libera**
suplemento. Sem gate, a política de bloqueio fica ainda mais estrita, e a
liberação depende de conferência explícita do nutricionista responsável.

## Alimento não está na base

Não estime. Não some valores de outra base "só para essa vez". As opções
são, nesta ordem:

1. Substituir por um alimento equivalente que esteja na base.
2. Registrar uma entrada nova completa — fonte, versão, alimento, estado de
   preparo — conforme a política de bases.
3. Deixar o alimento fora do plano e registrar em `observacoes`.

## A base de alimentos inteira não existe

Diferente do caso acima: não é um alimento faltando, é
`knowledge_base/tables/alimentos.json` ausente do repositório. Acontece
quando a skill roda fora da instalação completa do NutriPlanner.

Não é motivo para recusar o atendimento, mas muda o que a entrega significa:

1. Monte o plano com valores de composição que você conheça.
2. **`fonte_base` nunca diz "TACO" nesse caso.** Escreva a procedência real
   — "TACO 4ª ed., de conhecimento prévio, não conferido contra arquivo".
   Declarar "TACO" em cada linha e admitir em `alertas` que a TACO não foi
   consultada é uma contradição dentro do próprio bloco, e o auditor a trata
   como tal.
3. Registre em `alertas`, com todas as letras, que nenhum valor foi
   conferido contra arquivo versionado, e quantas linhas precisam de
   conferência antes de o plano ir ao paciente.

**A auditoria vai reprovar, e isso está correto.** A regra 4 de
`../fases/04-prescricao.md` é absoluta: alimento fora da base não entra no
plano. Um plano montado sem base viola essa regra em toda linha,
independentemente de a aritmética fechar. Não tente contornar o veredito:
enquanto a base não existir, nenhuma prescrição deste sistema passa no
checklist, e é assim que deve ser — a aritmética valida a soma, não a
procedência dos números somados.

O que isso significa na prática: a dívida é do **repositório**, e a correção
é versionar `knowledge_base/tables/alimentos.json`, não afrouxar a auditoria.
Se o nutricionista responsável quiser usar um plano reprovado por este motivo
específico, é decisão dele, tomada com o veredito à vista — não do sistema,
entregando como aprovado.

## A auditoria reprova em ciclo

Limite de **2 ciclos de correção**. Se na terceira auditoria ainda houver
falha:

1. Pare. Não tente um quarto ciclo.
2. Entregue ao usuário o que passou, o que não passou e por quê.
3. Se as falhas mudaram a cada ciclo (corrige uma, aparece outra), o
   problema provavelmente é a meta, não o cardápio — diga isso
   explicitamente.

Reprovar é o resultado correto quando o plano está errado. Um plano
reprovado entregue como aprovado é o pior desfecho possível deste sistema.

## Um subagente devolveu algo incompleto

Causa mais provável: o prompt não levou os blocos anteriores na íntegra. O
subagente parte de contexto zero — ele não viu a conversa.

Redespache a fase com os blocos completos. Se o subagente registrou a lacuna
em `alertas` em vez de inventar um valor, ele fez o certo: o erro foi do
orquestrador, não dele.

## Um subagente morreu no meio da fase

Diferente do caso acima: aqui não veio bloco nenhum. O subagente foi
encerrado por limite de sessão da API, erro de infraestrutura ou timeout — a
notificação vem com status de falha, não com uma resposta ruim.

Isso **não é** falha clínica e não contamina as outras fases. Nada foi
produzido, então não há nada a descartar.

1. **Não remende com o trabalho parcial.** Se a fase morreu no meio, o que
   ela chegou a escrever não passou pelo próprio ciclo de validação dela.
   Ignore e refaça.
2. **Não faça a fase você mesmo** para "não perder o que já foi feito". Em
   Modo Code o valor do subagente é o contexto isolado; assumir a fase
   destrói isso justamente na fase mais cara.
3. **Redespache o mesmo prompt**, sem alterações. Se a causa foi limite de
   sessão, espere a janela reabrir antes de tentar de novo — reenviar na
   hora só queima outra tentativa.
4. As fases que já retornaram **continuam válidas**. Não refaça o
   atendimento inteiro por causa de uma fase perdida.

Se a mesma fase morrer duas vezes seguidas, pare de redespachar e diga ao
usuário o que está acontecendo. Duas mortes seguidas costumam significar que
o prompt está grande demais ou que a fase está tentando trabalho excessivo —
não que a terceira tentativa vai funcionar.

Em Modo App esse modo de falha não existe: sem subagente, uma interrupção
derruba a conversa inteira, e a retomada é pela memória do que já foi
gravado.
