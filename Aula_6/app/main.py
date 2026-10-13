# Aula 6 - Construindo e Operacionalizando Pipeline de Previsão em Tempo Real

# Importa a biblioteca pandas para manipulação de dados
import pandas as pd

# Importa o framework FastAPI para construção da API
from fastapi import FastAPI

# Importa a classe de definição de entrada de dados do modelo
from app.modelo import InputData

# Importa a função personalizada para carregar o modelo e seus metadados
from app.utils import carrega_modelo_e_metadados

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Define uma rota de verificação de saúde do serviço
@app.get("/health")
def health_check():

    # Retorna o status do serviço
    return {"status": "ok"}

# Define uma rota para previsão
@app.post("/predict")
def predict(input_data: InputData):

    # Carrega o modelo treinado e seus metadados
    model, metadata = carrega_modelo_e_metadados()
    
    # Verifica se um modelo está disponível
    if model is None:

        # Retorna erro caso não haja modelo treinado
        return {"error": "Nenhum modelo treinado disponível"}
    
    # Cria um DataFrame a partir dos dados de entrada
    X = pd.DataFrame([[input_data.feature1, input_data.feature2, input_data.feature3]], 
                     columns = ["feature1", "feature2", "feature3"])
    
    # Realiza a previsão usando o modelo carregado
    prediction = model.predict(X)[0]
    
    # Retorna a previsão e a versão do modelo utilizado
    return {"Previsão": prediction, 
            "Versão do Modelo": metadata["version"], 
            "Versão do Scikit-Learn": metadata["scikit_learn_version"], 
            "Coeficiente R2 em Treino": metadata["r2_train"]}



