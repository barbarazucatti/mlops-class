# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo de Inferência

# Imports
import joblib
import pandas as pd

# Função para carregar o modelo treinado
def carrega_modelo(model_path):
    return joblib.load(model_path)

# Função para fazer previsão
def faz_previsao(model, features):
    predictions = model.predict(features)
    return predictions

# Função para executar as duas funções anteriores
def inferencia(model_path, features):
    model = carrega_modelo(model_path)
    predictions = faz_previsao(model, features)
    return predictions
