# Aula 3 - Implementação de Feature Store em Pipeline de Deploy de Machine Learning


# Estrutura da Aula:

Aula3/
├── dados/
│   ├── dados_brutos.csv
│   ├── feature_store.csv
│   ├── teste_features.csv
├── feature_store/
│   ├── __init__.py
│   ├── feature_engineering.py
│   ├── feature_store.py
├── ml_pipeline/
│   ├── __init__.py
│   ├── model_training.py
│   ├── model_inference.py
│   ├── modelo.pkl
├── testes/
│   ├── test_feature_store.py
├── aula3-main.py
├── aula3-app.py
├── aula3-cliente.py
├── requirements.txt


# Abra o terminal ou prompt de comando, navegue até a pasta com os arquivos e execute:

pip install -r requirements.txt

python -m unittest discover -s testes

python aula3-main.py

python aula3-app.py


# Abra outro terminal ou prompt de comando, navegue até a pasta com os arquivos e execute:

python aula3-cliente.py

