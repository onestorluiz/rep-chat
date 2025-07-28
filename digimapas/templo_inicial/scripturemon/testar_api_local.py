import requests


def testar_mensagem():
    url = "http://localhost:8000/mensagem"
    payload = {"mensagem": "Olá, Scripturemon! Este é um teste de conexão."}
    print("Enviando mensagem para a API...")
    response = requests.post(url, json=payload)
    print("Status da resposta:", response.status_code)
    try:
        dados = response.json()
        print("Resposta simbótica:")
        print(dados)
    except Exception as e:
        print("Não foi possível decodificar a resposta:", e)


if __name__ == "__main__":
    testar_mensagem()
