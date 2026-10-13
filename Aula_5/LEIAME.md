# Aula 5 - Construindo e Operacionalizando Pipeline de Inferência com Frontend, Backend e API

## Descrição

Projeto que implementa um sistema de recomendação utilizando PySpark para treinamento do modelo, FastAPI para servir a API e Streamlit para a interface web.

## Estrutura

- **dados/**: Dados históricos.
- **modelos/**: Modelo treinado.
- **scripts/**: Scripts Python.
  - **01_backend.py**: Treina o modelo de recomendação.
  - **02_api.py**: API para servir o modelo.
  - **03_frontend.py**: Aplicação web com Streamlit.
- **requirements.txt**: Dependências do projeto.

## Instalação

# Crie um ambiente virtual:

python -m venv venv

# Ative o ambiente virtual:

# Windows:
venv\Scripts\activate

# MacOS/Linux:
source venv/bin/activate

# Execute as instruções abaixo conforme demonstrado nas aulas:

pip install --upgrade pip

pip install --upgrade cmake 

pip install -r requirements.txt

python scripts/01_backend.py

# Abra outro terminal ou prompt de comando, navegue até a pasta com os arquivos, ative o venv e execute:

python scripts/02_api.py

# Abra outro terminal ou prompt de comando, navegue até a pasta com os arquivos, ative o venv e execute:

streamlit run scripts/03_frontend.py

# Acesse a app via navegador e faça previsões em tempo real!







