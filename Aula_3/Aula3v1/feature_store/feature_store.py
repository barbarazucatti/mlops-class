# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo de Criação da Feature Store

# Imports
import os
import pandas as pd

# Classe
class FeatureStore:

    # Construtor
    def __init__(self, feature_storage_path):
        self.feature_storage_path = feature_storage_path

    # Função para carregar features
    def carrega_atributos(self, entity_ids = None):
        features = pd.read_csv(self.feature_storage_path)
        if entity_ids:
            return features[features['entity_id'].isin(entity_ids)]
        return features

    # Função para salvar features
    def salva_atributos(self, df):
        df.to_csv(self.feature_storage_path, index = False)

    # Função para atualizar features
    def atualiza_atributos(self, df, entity_id):
        features = pd.read_csv(self.feature_storage_path)
        features.update(df[df['entity_id'] == entity_id])
        features.to_csv(self.feature_storage_path, index = False)
