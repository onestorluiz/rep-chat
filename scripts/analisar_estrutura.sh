#!/bin/bash
# Analisar estrutura atual do Digimundo

# Criar pasta de documentacao
mkdir -p documentacao

# Listar todos os arquivos .py
echo "Gerando lista de arquivos .py..."
find . -type f -name "*.py" > documentacao/lista_py.txt

# Contar linhas de codigo por arquivo e total
echo "Contando linhas de codigo..."
wc -l $(cat documentacao/lista_py.txt) > documentacao/contagem_linhas.txt

# Extrair imports unicos
echo "Coletando imports..."
grep -ho "^[[:space:]]*import [^ ]*" $(cat documentacao/lista_py.txt) | sort | uniq > documentacao/dependencias.txt

echo "Analise concluida. Resultados em documentacao/"
