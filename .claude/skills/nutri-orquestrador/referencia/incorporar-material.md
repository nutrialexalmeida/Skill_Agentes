# Incorporar material novo de `entrada/`

Leia quando o usuário pedir para processar a pasta `entrada/` (ou disser
"processa a entrada", "incorpora esses arquivos", "atualiza a skill com
isso").

## Sumário

- [Checklist do fluxo](#checklist-do-fluxo)
- [Passo 1: Inventariar](#passo-1-inventariar)
- [Passo 2: Classificar](#passo-2-classificar)
- [Passo 3: Questionar antes de aceitar](#passo-3-questionar-antes-de-aceitar)
- [Passo 4: Propor o destino](#passo-4-propor-o-destino)
- [Passo 5: Aplicar](#passo-5-aplicar)
- [Passo 6: Fechar o ciclo](#passo-6-fechar-o-ciclo)
- [Mapa de destinos](#mapa-de-destinos)

## Checklist do fluxo

Copie na sua resposta e marque conforme avança:

```
Incorporacao:
- [ ] Passo 1: Inventariar os arquivos de entrada/
- [ ] Passo 2: Classificar cada um
- [ ] Passo 3: Questionar o conteudo
- [ ] Passo 4: Propor destino e aguardar confirmacao
- [ ] Passo 5: Aplicar as mudancas
- [ ] Passo 6: Arquivar originais e registrar na memoria
```

## Passo 1: Inventariar

Liste o que há em `entrada/` (ignore `processados/` e `README.md`). Para
cada arquivo, registre nome, tipo e tamanho. Leia **integralmente** os que
forem texto — não decida o destino de um arquivo por amostragem.

Pasta vazia → diga isso e pare. Não invente trabalho.

## Passo 2: Classificar

Cada arquivo cai em uma destas categorias:

| Categoria | Exemplo |
|---|---|
| Regra clínica nova ou alterada | novo ponto de corte, nova contraindicação |
| Cálculo ou fórmula | equação nova, ajuste de fator de atividade |
| Referência científica | artigo, meta-análise, diretriz |
| Tabela de dados | composição de alimentos, faixas laboratoriais |
| Modelo de saída | template de plano, formato de relatório |
| Recomendação prática | conduta preferida, orientação ao paciente |
| Fora de escopo | não pertence a este sistema |

Um arquivo pode cair em mais de uma. Um PDF de diretriz pode trazer uma
regra clínica **e** a referência que a sustenta — nesse caso a regra vai
para a fase e a citação vai para `evidencias.md`.

## Passo 3: Questionar antes de aceitar

Material novo não entra só por ter sido colocado na pasta. Antes de propor
qualquer destino, verifique:

- **Origem.** Quem escreveu, quando, com que base? Sem fonte identificável,
  isso não vira regra — no máximo hipótese registrada, marcada como tal.
- **Conflito com o que já existe.** Contradiz alguma regra atual? Não
  sobrescreva em silêncio: **mostre o conflito** ao usuário e deixe a
  escolha com ele.
- **Força da evidência.** Meta-análise recente com amostra grande é uma
  coisa; post de blog é outra. Aplique os três níveis de
  `evidencias.md`.
- **Prazo de validade.** Diretriz tem versão. Se o material é atualização
  de algo que já está no sistema, confirme qual é a versão mais recente
  antes de trocar.
- **Segurança.** Material que afrouxa uma barreira de segurança (menor de
  idade, gestação, doença renal, transtorno alimentar) exige confirmação
  explícita do usuário e justificativa registrada. Nunca afrouxe uma
  barreira só porque um arquivo na pasta sugeriu isso.

Discordou do material? Diga. Aceitar acriticamente um arquivo é a forma mais
fácil de degradar a skill ao longo do tempo.

## Passo 4: Propor o destino

Apresente uma tabela: arquivo → categoria → destino proposto → o que muda.

**Espere confirmação antes de alterar regra clínica.** Adicionar uma
referência nova a `evidencias.md` é seguro e pode seguir direto; mudar um
ponto de corte em `../fases/02-calculo.md` não é.

## Passo 5: Aplicar

Uma regra tem **um** dono. Ao aplicar:

- Regra clínica → arquivo de fase correspondente. Nunca duplique dentro de
  `.claude/agents/*.md`, que são invólucros finos.
- Se a mudança cria algo que a auditoria precisa conferir, **atualize o
  checklist** em `../fases/05-auditoria.md`. Regra que a auditoria não confere
  é regra que na prática não existe.
- Se a mudança é aritmética verificável, considere estendê-la em
  `../scripts/validar_plano.py`, com um teste que a exercite.
- Conteúdo condicional (só relevante em alguns casos) → `referencia/`, e
  registre a linha correspondente no mapa de arquivos do `../SKILL.md`.

## Passo 6: Fechar o ciclo

1. Mova cada original para `entrada/processados/AAAA-MM/`.
2. Rode os evals (`../evals/`) se a mudança tocou regra de cálculo,
   distribuição ou auditoria.
3. Grave em `memoria/topicos/` o que foi incorporado, de onde veio e o que
   mudou.
4. Faça commit com o material e a mudança juntos, para que o histórico mostre
   a origem de cada regra.

## Mapa de destinos

| Categoria | Destino |
|---|---|
| Regra clínica | `../fases/NN-*.md` da fase correspondente |
| Cálculo / fórmula | `../fases/02-calculo.md`, e `scripts/` se for automatizável |
| Referência científica | `evidencias.md` |
| Tabela de dados | `knowledge_base/tables/` do NutriPlanner |
| Modelo de saída | `assets/template_dieta.md` |
| Recomendação prática | fase correspondente, ou `referencia/` se condicional |
| Regra de modo especial | `modos-especiais.md` |
| Problema recorrente | `troubleshooting.md` |
