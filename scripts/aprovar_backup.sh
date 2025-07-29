#!/bin/bash
if [ -z "$1" ]; then
  echo "⚠️  Use: bash scripts/aprovar_backup.sh digimundo_YYYY-MM-DD_HH-MM"
  exit 1
fi
cp -r "digimundo_autonomo/$1" "digimundo_aprovado/"
echo "✅ Backup $1 aprovado como versão simbólica estável"
