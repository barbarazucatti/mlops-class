# Aula 6 - Construindo e Operacionalizando Pipeline de Previsão em Tempo Real
# Módulo Cliente Para Consumo da API

# Import
import requests

# Função para testar a API
def testa_api():
    
    # URL do endpoint da API
    url = "http://localhost:8000/health"
    
    # Faz a chamada à API e armazena a resposta
    response = requests.get(url)
    
    # Imprime a resposta
    if response.status_code == 200:
        print("Status da saúde da API:", response.json())
    else:
        print(f"Erro ao checar saúde da API. Código de status: {response.status_code}")

# Função para consumir a API
def consome_api():
    
    # URL do endpoint da API
    url = "http://localhost:8000/predict"
    
    # Dados de entrada
    payload = {
        "feature1": 1.4,
        "feature2": 2.7,
        "feature3": 3.5
    }
    
    # Faz a chamada à API e armazena a resposta
    response = requests.post(url, json = payload)
    
    # Imprime a resposta
    if response.status_code == 200:
        print("Resposta da API:", response.json())
    else:
        print(f"Erro ao chamar a API. Código de status: {response.status_code}")

# Bloco principal
if __name__ == "__main__":
    testa_api()
    consome_api()



