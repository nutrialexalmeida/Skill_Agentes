#!/usr/bin/env bash
# Hook UserPromptSubmit: injeta a instrução de roteamento e o índice da
# memória persistente em toda mensagem enviada pelo usuário.

dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

cat <<'EOF'
[roteador] Antes de executar o pedido acima, siga a skill "roteador" (.claude/skills/roteador/SKILL.md):
1. Analise o pedido e identifique intenção, domínio e palavras-chave.
2. Consulte a memória persistente em memoria/ (índice abaixo) e carregue os tópicos relevantes de conversas anteriores.
3. Escolha a skill/ferramenta adequada e execute o pedido.
4. Ao concluir, atualize memoria/topicos/ e memoria/INDICE.md com decisões, trabalho feito e pendências.
EOF

if [ -f "$dir/memoria/INDICE.md" ]; then
  echo ""
  echo "=== ÍNDICE DA MEMÓRIA (memoria/INDICE.md) ==="
  cat "$dir/memoria/INDICE.md"
fi
