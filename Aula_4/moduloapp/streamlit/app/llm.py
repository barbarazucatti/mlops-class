# Aula 4 - Pipeline de MLOps Para Operacionalização e Monitoramento de IA Generativa com LLM e RAG

# Imports
import time
import hashlib
from app.connection import postgre_connection
from datetime import datetime
from transformers import pipeline

# Pipeline do modelo local, carregado sob demanda
qa_pipeline = None

# Função para gerar um ID único para o documento, combinando a consulta do usuário e a resposta gerada
def gera_documento_id(userQuery, answer):

    # Combina as primeiras 10 letras da consulta e da resposta para criar uma string única
    combined = f"{userQuery[:10]}-{answer[:10]}"
    
    # Gera um hash MD5 da string combinada
    hash_object = hashlib.md5(combined.encode())
    
    # Converte o hash em hexadecimal
    hash_hex = hash_object.hexdigest()
    
    # Extrai os primeiros 8 caracteres do hash para usar como ID do documento
    document_id = hash_hex[:8]
    
    # Retorna o ID do documento
    return document_id

# Função para realizar uma consulta no modelo de linguagem local com o payload fornecido
def query(payload):

    # Carrega o modelo BERT (LLM) localmente na primeira chamada e reutiliza nas seguintes
    # https://huggingface.co/google-bert/bert-large-uncased-whole-word-masking-finetuned-squad
    global qa_pipeline
    if qa_pipeline is None:
        qa_pipeline = pipeline("question-answering", model="google-bert/bert-large-uncased-whole-word-masking-finetuned-squad")

    # Inicia a contagem de tempo para medir o tempo de resposta
    start_time = time.time()

    # Executa a inferência local com a pergunta e o contexto do payload
    response = qa_pipeline(**payload["inputs"])

    # Finaliza a contagem de tempo ao receber a resposta
    end_time = time.time()

    # Calcula o tempo de resposta, arredondando para 2 casas decimais
    responseTime = round(end_time - start_time, 2)

    # Retorna a resposta do modelo (dict com 'answer' e 'score') e o tempo de resposta
    return response, responseTime

# Função para capturar a entrada do usuário e salvar os dados de avaliação no banco de dados
def captura_user_input(docId, userQuery, result, llmScore, responseTime, hit_rate, mrr):

    # Estabelece a conexão e o cursor com o banco de dados PostgreSQL
    conn, cur = postgre_connection()
    
    try:
        # Define a query SQL para criar a tabela de avaliação, se ainda não existir
        create = """
            CREATE TABLE avaliacao (
                id SERIAL PRIMARY KEY,
                doc_id VARCHAR(10) NOT NULL,
                user_input TEXT NOT NULL,
                result TEXT NOT NULL,
                llm_score DOUBLE PRECISION NOT NULL,
                response_time DOUBLE PRECISION NOT NULL,
                hit_rate_score DOUBLE PRECISION NOT NULL,
                mrr_score DOUBLE PRECISION NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        # Executa a query de criação da tabela
        cur.execute(create)

    except Exception as e:
        # Em caso de erro, imprime a exceção e desfaz a transação
        print(e)
        conn.rollback() 

    try:

        # Define a query SQL para inserir os dados de avaliação na tabela
        sql = f"""
            INSERT INTO avaliacao
            (doc_id, user_input, result, llm_score, response_time, hit_rate_score, mrr_score)
            VALUES
            ('{docId}', '{userQuery}', '{result}', {llmScore}, {responseTime}, {hit_rate}, {mrr})
        """

        # Executa a query de inserção
        cur.execute(sql)

    except Exception as e:
        # Em caso de erro, imprime a exceção e desfaz a transação
        print(e)
        conn.rollback() 

    # Confirma as operações e fecha a conexão com o banco de dados
    conn.commit()
    cur.close()
    conn.close()
    
    # Retorna uma mensagem de confirmação da inserção
    return "Dados de Avaliação Inseridos"

# Função para capturar o feedback do usuário e salvar no banco de dados
def captura_user_feedback(docId, userQuery, result, feedback):

    # Estabelece a conexão e o cursor com o banco de dados PostgreSQL
    conn, cur = postgre_connection()
    
    try:

        # Define a query SQL para criar a tabela de feedback, se ainda não existir
        create = """
            CREATE TABLE feedback (
                id SERIAL PRIMARY KEY,
                doc_id VARCHAR(10) NOT NULL,
                user_input TEXT NOT NULL,
                result TEXT NOT NULL,
                is_satisfied BOOLEAN NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        # Executa a query de criação da tabela
        cur.execute(create)

    except Exception as e:
        # Em caso de erro, imprime a exceção e desfaz a transação
        print(e)
        conn.rollback() 

    try:

        # Define a query SQL para inserir os dados de feedback na tabela
        sql = f"""
            INSERT INTO feedback
            (doc_id, user_input, result, is_satisfied)
            VALUES
            ('{docId}', '{userQuery}', '{result}', {feedback})
        """

        # Executa a query de inserção
        cur.execute(sql)

    except Exception as e:
        # Em caso de erro, imprime a exceção e desfaz a transação
        print(e)
        conn.rollback() 

    # Confirma as operações e fecha a conexão com o banco de dados
    conn.commit()
    cur.close()
    conn.close()

    # Retorna uma mensagem de confirmação da inserção
    return "Dados de Feedback Inseridos"
