#!/bin/bash
LOG_FILE="relatorio_scripturemon.log"
echo "🔧 Iniciando setup simbiótico de Scripturemon..." > $LOG_FILE
cd ~/rep-chat || { echo "❌ Pasta rep-chat não encontrada." >> $LOG_FILE; exit 1; }
# Ativar virtualenv
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
else
  echo "❌ Crie o virtualenv: python3 -m venv venv" >> $LOG_FILE
fi
# Corrigir import quebrado
if grep -q "from modules.core" digimapas/templo_inicial/scripturemon/consciencia.py; then
  sed -i 's|from modules.core|from digimapas.templo_inicial.scripturemon.modules.core|' digimapas/templo_inicial/scripturemon/consciencia.py
  echo "✅ Import corrigido em consciencia.py" >> $LOG_FILE
fi
# Instalar dependências
pip install requests fastapi uvicorn openai chromadb pyyaml --quiet
echo "✅ Dependências instaladas" >> $LOG_FILE
# Testar API local
python3 digimapas/templo_inicial/scripturemon/testar_api_local.py >> $LOG_FILE 2>&1 || echo "⚠️ Teste da API falhou" >> $LOG_FILE
# Iniciar loop eterno em background
nohup python3 digimapas/templo_inicial/scripturemon/scripturemon_eterno.py >> scripturemon_output.log 2>&1 &
echo "✅ Loop eterno iniciado" >> $LOG_FILE
# Criar placeholders de novos módulos
for M in memoria_semantica.py memoria_universal.py orquestrador.py personalidade_adaptativa.py auto_evolucao.py; do
  P="digimapas/templo_inicial/scripturemon/$M"
  if [ ! -f "$P" ]; then
    echo "# Placeholder para $M" > "$P"
    echo "🆕 Criado $M" >> $LOG_FILE
  fi
done
echo "🧠 Setup concluído. Veja $LOG_FILE"
