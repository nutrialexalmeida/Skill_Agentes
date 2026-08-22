# Contrato de handoff entre as fases

## Sumário

- [Regras gerais](#regras-gerais)
- [ANAMNESE (fase 1)](#anamnese-fase-1)
- [EXAMES (fase 2a)](#exames-fase-2a)
- [CALCULO (fase 2b)](#calculo-fase-2b)
- [SUPLEMENTACAO (fase 3a)](#suplementacao-fase-3a)
- [PRESCRICAO (fase 3b)](#prescricao-fase-3b)
- [AUDITORIA (fase 4)](#auditoria-fase-4)

Toda fase termina emitindo um bloco JSON com a chave que leva seu nome.
Esses blocos são o único meio de comunicação entre as fases — em Modo Code
porque o subagente não vê a conversa, e em Modo App para que a auditoria
tenha o que conferir sem depender de memória.

## Regras gerais

- Campo desconhecido → `null`. Nunca invente valor para preencher schema.
- Campo que a fase decidiu não aplicar → preencha e explique em
  `observacoes`.
- Nenhuma fase pode alterar bloco de outra fase. Discordou? Registre em
  `alertas` e devolva ao orquestrador.

## ANAMNESE (fase 1)

```json
{
  "ANAMNESE": {
    "idade": 0, "sexo": "", "peso_kg": 0, "altura_cm": 0,
    "objetivo": "", "rotina": "", "atividade_fisica": "",
    "n_refeicoes": 0,
    "preferencias": [], "restricoes": [],
    "condicoes_clinicas": [], "medicamentos": [],
    "contexto_social": "",
    "exames_disponiveis": true,
    "modo": "padrao | pre_pos_treino | competicao",
    "triagem_seguranca": {
      "bloqueado": false,
      "motivo": null
    },
    "dados_essenciais_confirmados": true,
    "observacoes": ""
  }
}
```

## EXAMES (fase 2a)

```json
{
  "EXAMES": {
    "disponivel": true,
    "data_coleta": null,
    "marcadores": [
      {"nome": "", "valor": 0, "unidade": "", "referencia": "",
       "situacao": "dentro | abaixo | acima", "relevancia_nutricional": ""}
    ],
    "implicacoes_para_o_plano": [],
    "exames_recomendados": [],
    "alertas": [],
    "observacoes": ""
  }
}
```

## CALCULO (fase 2b)

```json
{
  "CALCULO": {
    "equacao_usada": "",
    "justificativa_da_equacao": "",
    "ger_tmb_kcal": 0,
    "get_kcal": 0,
    "meta_energetica_kcal": 0,
    "macros": {
      "proteina": {"g_dia": 0, "g_kg": 0},
      "carboidrato": {"g_dia": 0, "g_kg": 0},
      "gordura": {"g_dia": 0, "g_kg": 0}
    },
    "metas_por_refeicao": [
      {"refeicao": "", "ordem": 1, "kcal": 0,
       "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0}
    ],
    "guardrails": {
      "proteina_g_kg_minima_respeitada": true,
      "meta_abaixo_do_guardrail": false,
      "justificativa": null
    },
    "alertas": [],
    "observacoes": ""
  }
}
```

## SUPLEMENTACAO (fase 3a)

```json
{
  "SUPLEMENTACAO": {
    "avaliados": [
      {"item": "", "veredito": "liberado | bloqueado",
       "motivo": "", "nivel_evidencia": "A | B | C | D",
       "fonte": "", "aprovacao_profissional_necessaria": true}
    ],
    "alertas": [],
    "observacoes": ""
  }
}
```

## PRESCRICAO (fase 3b)

```json
{
  "PRESCRICAO": {
    "modo": "padrao | pre_pos_treino | competicao",
    "justificativa_da_excecao": null,
    "refeicoes": [
      {"nome": "", "ordem": 1, "horario_sugerido": "",
       "alimentos": [
         {"alimento": "", "fonte_base": "TACO",
          "medida_caseira": "", "gramas": 0,
          "kcal": 0, "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0}
       ],
       "totais": {"kcal": 0, "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0}}
    ],
    "totais_dia": {"kcal": 0, "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0},
    "substituicoes": [
      {"refeicao": "", "original": "", "original_g": 0,
       "substituto": "", "substituto_g": 0, "medida_caseira": ""}
    ],
    "alertas": [],
    "observacoes": ""
  }
}
```

## AUDITORIA (fase 4)

```json
{
  "AUDITORIA": {
    "veredito": "aprovado | reprovado",
    "itens": [
      {"item": "", "resultado": "passou | falhou",
       "evidencia": "", "fase_responsavel": ""}
    ],
    "falhas": [
      {"descricao": "", "fase_responsavel": "", "correcao_sugerida": ""}
    ],
    "observacoes": ""
  }
}
```
