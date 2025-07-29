#!/bin/bash

# Caminho do repositório
REPO_PATH="/root/rep-chat"

# Entrar na pasta do repositório
cd "$REPO_PATH" || exit

# Verificar se há mudanças
CHANGES=$(git status --porcelain)

if [ -n "$CHANGES" ]; then
  echo "🔍 Mudanças detectadas:"
  echo "$CHANGES"
  
  # Adicionar tudo ao git
  git add .

  # Criar mensagem de commit simbólica com timestamp
  NOW=$(date "+%Y-%m-%d %H:%M")
  git commit -m "📜 Atualização simbiótica automática — $NOW"

  # Push para o GitHub
  git push origin main

  echo "✅ Sincronização simbiótica concluída."
else
  echo "🧘 Nenhuma mudança detectada. Nada a sincronizar."
fi
