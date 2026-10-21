# Aula 4 - Pipeline de MLOps Para Operacionalização e Monitoramento de IA Generativa com LLM e RAG

# Importa o módulo DAG do Airflow para criar e gerenciar DAGs (fluxos de trabalho)
from airflow import DAG

# Importa days_ago para definir datas de início relativas
from airflow.utils.dates import days_ago

# Importa o operador PythonOperator para executar funções Python como tarefas
from airflow.operators.python import PythonOperator

# Importa timedelta para definir intervalos de tempo para tentativas de reexecução
from datetime import timedelta

# Importa funções personalizadas para manipulação de dados do módulo 'modulodados'
from modulodados.carrega_dados import cria_tabela, insere_dados_json, insere_dados_csv, cria_indice

# Define argumentos padrão para as tarefas do DAG
defaultArguments = {
    "owner": "airflow",             # Nome do proprietário do DAG
    "start_date": days_ago(1),         # Define a data de início como um dia atrás
    "retries": 1,                      # Número de tentativas de reexecução em caso de falha
    "retry_delay": timedelta(hours=1)  # Intervalo de uma hora entre tentativas de reexecução
}

# Cria a DAG com o nome 'Carrega_Dados_LLM'
dag = DAG(
    "Carrega_Dados_RAG",
    default_args=defaultArguments,                       # Usa os argumentos padrão definidos acima
    schedule_interval="0 0 * * *",                       # Define a execução diária à meia-noite
    description="Carrega os dados para o módulo de RAG"  # Descrição da DAG
)

# Define a tarefa para criar a tabela, usando a função 'cria_tabela' do módulo
tarefa_cria_tabela = PythonOperator(
    task_id="tarefa_cria_tabela",     # Identificador único da tarefa
    python_callable=cria_tabela,  # Função Python a ser executada
    dag=dag                           # DAG a qual a tarefa pertence
)

# Define a tarefa para carregar dados JSON, usando a função 'insere_dados_json'
tarefa_carrega_json = PythonOperator(
    task_id="tarefa_carrega_json",          # Identificador único da tarefa
    python_callable=insere_dados_json,  # Função Python a ser executada
    dag=dag                                 # DAG a qual a tarefa pertence
)

# Define a tarefa para carregar dados CSV, usando a função 'insere_dados_csv'
tarefa_carrega_csv = PythonOperator(
    task_id="tarefa_carrega_csv",          # Identificador único da tarefa
    python_callable=insere_dados_csv,  # Função Python a ser executada
    dag=dag                                # DAG a qual a tarefa pertence
)

# Define a tarefa para criar o índice, usando a função 'cria_indice'
tarefa_cria_indice = PythonOperator(
    task_id="tarefa_cria_indice",     # Identificador único da tarefa
    python_callable=cria_indice,  # Função Python a ser executada
    dag=dag                           # DAG a qual a tarefa pertence
)

# Define a ordem de execução das tarefas na DAG
# Primeiro cria a tabela, depois carrega os dados JSON, seguido pelos dados CSV, e por último cria o índice no ElasticSearch
# Isso define a estratégia de RAG
tarefa_cria_tabela >> tarefa_carrega_json >> tarefa_carrega_csv >> tarefa_cria_indice




