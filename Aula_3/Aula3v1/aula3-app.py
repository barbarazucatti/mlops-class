# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning
# Módulo de Deploy do Modelo via API

# Imports
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Cria a app
app = Flask(__name__)

# Carrega o modelo treinado
MODEL_PATH = 'ml_pipeline/modelo.pkl'

# Bloco try/except
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print("Erro: Modelo não encontrado.")

# Endpoint para prever novos dados
@app.route('/predict', methods = ['POST'])
def predict():
    try:

        # Obter os dados do request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400

        # Converter para DataFrame do pandas
        df = pd.DataFrame(data)

        # Remover colunas desnecessárias
        if 'entity_id' in df.columns:
            df = df.drop(columns=['entity_id'])

        if 'target' in df.columns:
            df = df.drop(columns=['target'])

        if model:

            # Fazer a predição
            predictions = model.predict(df)
            return jsonify({'predictions': predictions.tolist()})
        else:
            return jsonify({'error': 'Modelo não carregado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = False)





