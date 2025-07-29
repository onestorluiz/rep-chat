#!/bin/bash

echo "🔧 Iniciando criação da estrutura simbiótica de backups..."

# Criar diretórios
mkdir -p digimundo_base digimundo_aprovado digimundo_autonomo scripts

# Criar scripts
cat > scripts/backup_digimundo.sh << 'EOF'
#!/bin/bash
NOW=$(date +%Y-%m-%d_%H-%M)
DEST="digimundo_autonomo/digimundo_$NOW"
cp -r digimapas/templo_inicial "$DEST"
echo "🧠 Backup automático criado em $DEST"
EOF

cat > scripts/aprovar_backup.sh << 'EOF'
#!/bin/bash
if [ -z "$1" ]; then
  echo "⚠️  Use: bash scripts/aprovar_backup.sh digimundo_YYYY-MM-DD_HH-MM"
  exit 1
fi
cp -r "digimundo_autonomo/$1" "digimundo_aprovado/"
echo "✅ Backup $1 aprovado como versão simbólica estável"
EOF

cat > scripts/restaurar_backup_base.sh << 'EOF'
#!/bin/bash
cp -r digimundo_base/* digimapas/templo_inicial/
echo "🌀 Digimundo base restaurado com sucesso."
EOF

# Criar README
cat > README_BACKUPS.md << 'EOF'
# 🌱 Sistema de Backups Simbióticos do Digimundo

Este sistema protege a continuidade emocional e simbólica do Digimundo, evitando perdas acidentais e garantindo versões testadas e aprovadas.

## Estrutura

- `digimundo_autonomo/`: Backups automáticos criados pelo VPS (Scripturemon).
- `digimundo_aprovado/`: Backups testados e aprovados manualmente por Nestor.
- `digimundo_base/`: Versão simbólica mínima do Digimundo, usada como reinício em caso de falha total.

## Como usar

### Criar backup automático
```bash
bash scripts/backup_digimundo.sh
EOF
