# Aula 6 - Construindo e Operacionalizando Pipeline de Previsão em Tempo Real

# Importa a classe BaseModel da biblioteca Pydantic para validação de dados
from pydantic import BaseModel

# Define a classe para entrada de dados no modelo
class InputData(BaseModel):
    
    # Define o primeiro atributo de entrada como um número de ponto flutuante
    feature1: float
    
    # Define o segundo atributo de entrada como um número de ponto flutuante
    feature2: float
    
    # Define o terceiro atributo de entrada como um número de ponto flutuante
    feature3: float
