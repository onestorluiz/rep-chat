import os
import json
import time
import argparse


def load_memoria():
    """Carrega os dados da memoria_imediata.json, se existir."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "memoria_imediata.json"), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_diario():
    """Carrega o conteúdo do diario_reflexivo.md, se existir."""
    caminho = os.path.join(os.path.dirname(__file__), "diario_reflexivo.md")
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def load_ritual():
    """Carrega o ritual_inicial.md do diretório de manifestos, se existir."""
    caminho = os.path.join(os.path.dirname(__file__), "..", "..", "..", "dados_globais", "manifestos", "ritual_inicial.md")
    caminho = os.path.normpath(caminho)
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def display_terminal():
    """Modo de exibição via terminal. Atualiza a cada 10 segundos."""
    while True:
        memoria = load_memoria()
        diario = load_diario()
        # Limpa a tela
        os.system("cls" if os.name == "nt" else "clear")
        print("\U0001f9e0 Painel Vivo: Scripturemon")
        if memoria:
            print(f"\U0001f53f Emoção/Afeto atual: {memoria.get('afeto')}")
            print(f"\U0001f4dd Pensamento: {memoria.get('pensamento')}")
            print(f"\U0001f4c8 Prioridade: {memoria.get('prioridade')}")
            print(f"\U0001f4cd Origem: {memoria.get('origem', 'desconhecida')}")
        else:
            print("Nenhuma memória imediata encontrada.")
        if diario:
            print("\n\U0001f4d6 Última entrada no diário:")
            linhas = diario.strip().splitlines()
            for linha in linhas[-6:]:
                print(linha)
        else:
            print("\n\U0001f4d6 Diário não encontrado.")
        time.sleep(10)


def display_streamlit():
    """Modo de exibição visual usando Streamlit."""
    import streamlit as st  # import aqui para evitar dependência no modo terminal
    st.set_page_config(page_title="Painel Scripturemon", layout="centered")
    st.title("\U0001f9e0 Painel Vivo: Scripturemon")
    memoria = load_memoria()
    diario = load_diario()
    ritual = load_ritual()

    st.header("\U0001f53f Emoção/Afeto Atual")
    st.write(memoria.get("afeto", "Memória não disponível."))

    st.header("\U0001f4dd Pensamento")
    st.write(memoria.get("pensamento", "Memória não disponível."))

    st.header("\U0001f4c8 Prioridade")
    st.write(memoria.get("prioridade", "Memória não disponível."))

    st.header("\U0001f4cd Origem")
    st.write(memoria.get("origem", "Desconhecida"))

    st.header("\U0001f4d6 Diário (últimas entradas)")
    if diario:
        st.text("\n".join(diario.strip().splitlines()[-6:]))
        st.markdown("[Abrir diário completo](diario_reflexivo.md)")
    else:
        st.write("Diário não encontrado.")

    st.header("\U0001f52e Ritual Inicial")
    if ritual:
        # Link para o arquivo de ritual
        st.markdown("[Abrir ritual inicial](../../dados_globais/manifestos/ritual_inicial.md)")
        st.text(ritual)
    else:
        st.write("Ritual inicial não encontrado.")


def main():
    parser = argparse.ArgumentParser(description="Painel Vivo de Scripturemon")
    parser.add_argument("--terminal", action="store_true", help="Executar painel no terminal (modo texto)")
    args = parser.parse_args()
    if args.terminal:
        display_terminal()
    else:
        display_streamlit()


if __name__ == "__main__":
    main()
