#!/bin/bash
NOW=$(date +%Y-%m-%d_%H-%M)
DEST="digimundo_autonomo/digimundo_$NOW"
cp -r digimapas/templo_inicial "$DEST"
echo "🧠 Backup automático criado em $DEST"
