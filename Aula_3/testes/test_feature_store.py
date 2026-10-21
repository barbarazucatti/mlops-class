# Projeto 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo de Teste da Feature Store

# Imports
import unittest
import pandas as pd
from mlops.Aula_3.feature_store.feature_store import FeatureStore

# Classe
class TestFeatureStore(unittest.TestCase):

    def setUp(self):

        # Criação de um arquivo temporário de features
        self.feature_path = 'dados/teste_features.csv'

        # Criação do dataframe com dados de exemplo
        self.df = pd.DataFrame({
            'entity_id': [1, 2, 3],
            'feature1': [0.5, 0.7, 0.2],
            'feature2': [0.1, 0.3, 0.4]
        })

        # Salva os dados
        self.df.to_csv(self.feature_path, index = False)

        # Armazena na Feature Store
        self.store = FeatureStore(self.feature_path)

    def testa_carrega_atributos(self):
        features = self.store.carrega_atributos()
        self.assertEqual(len(features), 3)

    def testa_atualiza_atributos(self):
        new_df = pd.DataFrame({
            'entity_id': [1],
            'feature1': [0.9],
            'feature2': [0.8]
        })
        
        self.store.atualiza_atributos(new_df, 1)
        
        updated_features = self.store.carrega_atributos(entity_ids = [1])
        
        self.assertEqual(updated_features.iloc[0]['feature1'], 0.9)

if __name__ == '__main__':
    unittest.main()
