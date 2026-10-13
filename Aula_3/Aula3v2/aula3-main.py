# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo Principal

# Imports
import os
from feature_store.feature_engineering import carrega_dados, cria_atributos, salva_atributos
from feature_store.feature_store import FeatureStore
from ml_pipeline.model_training import treina_modelo
from ml_pipeline.model_inference import inferencia

# Caminhos de arquivos
RAW_DATA_PATH = 'dados/dados_brutos.csv'
FEATURE_STORE_PATH = 'dados/feature_store.csv'
MODEL_PATH = 'ml_pipeline/modelo.pkl'

# Bloco principal
def main():

    # Ingestão dos dados brutos
    raw_data = carrega_dados(RAW_DATA_PATH)

    # Criação dos atributos
    features = cria_atributos(raw_data)
    
    # Cria instância da Feature Store
    feature_store = FeatureStore(FEATURE_STORE_PATH)

    # Salva os dados processados na Feature Store
    feature_store.salva_atributos(features)

    # Treina o modelo com as features armazenadas na Feature Store
    # Observe que a variável target não fica na Feature Store
    labels = raw_data['target']  
    treina_modelo(labels, MODEL_PATH)

    # Carrega os atributos da Feature Store para inferência
    new_features = feature_store.carrega_atributos()

    # Faz a inferência extraindo as previsões com os atributos da feature store
    predictions = inferencia(MODEL_PATH, new_features)
    print(f"Previsões: {predictions}")

if __name__ == '__main__':
    main()
