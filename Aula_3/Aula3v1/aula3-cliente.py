# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo de Consumo da API

# Imports
import requests

# Dados para previsão 
novos_dados = [
    {"entity_id": 1000, "feature1": 14.2, "feature2": 4.5, "time_diff": 3600},
]

# URL da API
url = 'http://127.0.0.1:5000/predict'

# Fazer a requisição POST
response = requests.post(url, json = novos_dados)

# Verificar o código de status da resposta
print(f"\nStatus Code: {response.status_code}")
print(f"Resposta da API:\n")

# Tentar fazer o parse de JSON se o status for 200
if response.status_code == 200:
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Erro ao interpretar a resposta como JSON.")
else:
    print("Erro na requisição")

print(f"\nObrigado Por Usar Este Pipeline de MLOps!\n")