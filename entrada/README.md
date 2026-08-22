# entrada/ — materiais novos para incorporar às skills

Solte aqui qualquer arquivo que deva virar conhecimento do sistema: novos
cálculos, atualizações de diretriz, artigos, tabelas, modelos de saída,
recomendações, exemplos de plano, planilhas, PDFs.

Depois é só dizer, em qualquer conversa: **"processa a entrada"**.

Você não precisa organizar nada antes de soltar. Classificar e decidir onde
cada coisa se encaixa é trabalho do Claude, não seu.

## Como funciona

O Claude segue o fluxo de
`.claude/skills/nutri-orquestrador/referencia/incorporar-material.md`:

1. Lê o que está aqui e classifica cada arquivo.
2. **Propõe** onde cada coisa entra — e espera sua confirmação antes de
   alterar regra clínica.
3. Aplica no lugar certo da skill.
4. Move o original para `entrada/processados/AAAA-MM/`, para você saber o
   que já foi absorvido.

Nada é incorporado em silêncio: toda mudança de regra clínica passa por
você.

## O que ajuda (mas não é obrigatório)

- Um bilhete junto — `.txt` ou no nome do arquivo — dizendo o que você quer
  que aconteça. "Substituir a tabela atual" e "considerar como alternativa"
  levam a lugares bem diferentes.
- A fonte, quando for material científico. Diretriz sem origem não vira
  regra: vira, no máximo, hipótese registrada.
- A data, quando for atualização de algo que já existe.

## O que NÃO colocar aqui

- **Dados de paciente real.** Este repositório é versionado em git; o que
  entra fica no histórico. Para caso clínico, use dados anonimizados.
- Arquivo que você quer só que eu leia uma vez — para isso, anexe direto na
  conversa. Esta pasta é para o que deve virar conhecimento permanente.

## Estrutura

```
entrada/
  README.md              este arquivo
  processados/           originais já incorporados, por mês
```
