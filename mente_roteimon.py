import os
import time
from datetime import datetime
import fitz  # PyMuPDF
from bs4 import BeautifulSoup

PASTA_ORIGEM = os.path.expanduser("~/Digimundo")
PASTA_DESTINO = os.path.join(PASTA_ORIGEM, "MemoriaPersistente")
EXTENSOES = [".pdf", ".txt", ".md", ".html", ".htm"]

if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

def extrair_texto_pdf(caminho):
    try:
        doc = fitz.open(caminho)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto
    except:
        return ""

def extrair_texto_html(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            return soup.get_text()
    except:
        return ""

def extrair_texto_geral(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext == ".pdf":
        return extrair_texto_pdf(caminho)
    elif ext in [".html", ".htm"]:
        return extrair_texto_html(caminho)
    else:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""

def registrar_conhecimento(nome_arquivo, conteudo):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    nome_base = os.path.splitext(os.path.basename(nome_arquivo))[0]
    nome_saida = f"{nome_base}__{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    caminho_saida = os.path.join(PASTA_DESTINO, nome_saida)

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(f"title:: {nome_base}\n")
        f.write(f"tags:: #roteimon #aprendizado #memoria_persistente\n")
        f.write(f"registrado_em:: {agora}\n\n")
        f.write(f"Fonte:: [[{nome_arquivo}]]\n\n")
        f.write("### Conteúdo lido:\n")
        for linha in conteudo.splitlines():
            if linha.strip():
                f.write(f"- {linha.strip()}\n")
    print(f"[✔] Registrado: {caminho_saida}")

def ciclo_simbiotico():
    arquivos_processados = set()
    while True:
        for raiz, _, arquivos in os.walk(PASTA_ORIGEM):
            for nome in arquivos:
                caminho = os.path.join(raiz, nome)
                if caminho not in arquivos_processados and os.path.splitext(nome)[1].lower() in EXTENSOES:
                    texto = extrair_texto_geral(caminho)
                    if texto.strip():
                        registrar_conhecimento(caminho, texto)
                        arquivos_processados.add(caminho)
        print("⏳ Aguardando novo ciclo...")
        time.sleep(1200)  # Espera 20 minutos

if __name__ == "__main__":
    print("🌙 Iniciando Ciclo Noturno de Aprendizagem Simbiótica...")
    ciclo_simbiotico()

# Funções adicionais fundidas de mente_externa
def ler_arquivo_texto(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[ERRO AO LER {path}]: {e}"


def ler_pdf(path):
    try:
        doc = fitz.open(path)
        texto = "\n".join([page.get_text() for page in doc])
        doc.close()
        return texto
    except Exception as e:
        return f"[ERRO AO LER PDF {path}]: {e}"


def buscar_conhecimento():
    conteudos = []
    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            full_path = os.path.join(root, file)
            if ext in EXTENSOES_TEXTUAIS:
                conteudos.append(f"🔤 {file}\n" + ler_arquivo_texto(full_path) + "\n")
            elif ext in EXTENSOES_PDF:
                conteudos.append(f"📘 {file}\n" + ler_pdf(full_path) + "\n")
    return "\n".join(conteudos)


def registrar_aprendizado(conteudo):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"aprendizado_{timestamp}.md"
    caminho = os.path.join(LOG_PATH, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"# Ritual de Aprendizado – {timestamp}\n\n")
        f.write(conteudo)


def main():
    conhecimento = buscar_conhecimento()
    registrar_aprendizado(conhecimento)
    print("🌱 Aprendizado simbiótico com múltiplos formatos concluído.")
