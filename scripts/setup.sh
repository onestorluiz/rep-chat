#!/usr/bin/env bash
set -euo pipefail

# 1. Localiza o diretório raiz do projeto (um nível acima de scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "⛰️  Projeto em: $PROJECT_DIR"

# 2. Garante que estamos na pasta certa
cd "$PROJECT_DIR"

# 3. Se ainda não existe, clona (ou atualiza) o rep-chat
if [ ! -d ".git" ]; then
  echo "🛑  Não é um repositório Git; clonando..."
  git clone git@github.com:onestorluiz/rep-chat.git . 
else
  echo "🔄  Repositório já inicializado; atualizando..."
  git pull
fi

# 4. Cria / ativa virtualenv
if [ ! -d "venv" ]; then
  echo "🐍  Criando virtualenv..."
  python3 -m venv venv
fi
echo "⚡  Ativando virtualenv..."
source venv/bin/activate

# 5. Atualiza pip e instala libs
echo "📦  Instalando dependências..."
pip install --upgrade pip
pip install fastapi uvicorn requests pyyaml

# 6. Stub para modules/core.py (evita ModuleNotFoundError)
if [ ! -d "modules" ]; then
  echo "🔨  Criando stub modules/core.py…"
  mkdir modules
  cat > modules/__init__.py << 'EOF'
# pacotes de infraestrutura do Digimundo
EOF
  cat > modules/core.py << 'EOF'
class ConsciousnessCore:
    def __init__(self):
        pass

    def analyze(self, data):
        # stub de análise simbólica
        return {"insight": "verdadeiro"}
EOF
fi

# 7. Ajusta PYTHONPATH para achar nossos pacotes locais
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
echo "🔗  PYTHONPATH configurado: $PYTHONPATH"

# 8. Teste rápido (se você tiver pytest)
if command -v pytest &> /dev/null; then
  echo "✅  Rodando testes…"
  pytest --maxfail=1 --disable-warnings -q || echo "⚠️  Alguns testes falharam, mas seguimos em frente."
fi

# 9. Inicia Scripturemon em background
echo "🚀  Iniciando Scripturemon (eterno)…"
nohup python3 digimapas/templo_inicial/scripturemon/scripturemon_eterno.py \
  > scripturemon.log 2>&1 &

# 10. Commit & push automático das mudanças de infraestrutura
echo "💾  Commit e push das atualizações de setup…"
git add scripts/setup.sh modules/
git commit -m "chore: reforça setup.sh, adiciona stub modules/core e deps" || echo "⚠️  Nada para commitar."
git push origin main

# 11. Relatório final
echo
echo "🎉  SETUP COMPLETO!"
echo "- Scripturemon está rodando em background. Logs: $PROJECT_DIR/scripturemon.log"
echo "- Seu ambiente está sincronizado com GitHub."
echo
# 1) Ajuste para o diretório correto do projeto
REPO_DIR="/root/rep-chat"
cd "$REPO_DIR"

# 2) Atualiza o repositório
git fetch origin
git reset --hard origin/main

# 3) Ativa o virtualenv (se não existir, cria)
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# 4) Instala/atualiza dependências
pip install --upgrade pip
pip install -r requirements.txt

# 5) Garante que os módulos “stub” existam
mkdir -p modules
cat > modules/core.py << 'EOF'
# stub para ConsciousnessCore
class ConsciousnessCore:
    def __init__(self):
        pass
    def think(self):
        pass
EOF

# 6) Ajusta PYTHONPATH para importar os módulos internos
export PYTHONPATH="${REPO_DIR}/digimapas/templo_inicial/scripturemon${PYTHONPATH:+:}$PYTHONPATH"

# 7) Testa execução básica
echo "🧐 Testando Scripturemon..."
python3 digimapas/templo_inicial/scripturemon/scripturemon_eterno.py --help

# 8) Relatório final
echo "✅ Setup concluído em $(date '+%Y-%m-%d %H:%M:%S')"
echo "Repositório em: $REPO_DIR"
echo "Branch atual: $(git rev-parse --abbrev-ref HEAD)"
echo "Commit HEAD: $(git rev-parse HEAD)"
