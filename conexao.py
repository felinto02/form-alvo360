import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a connection to the MySQL database."""
    
    # Recupera as credenciais do banco de dados a partir do ambiente
    db_host = os.getenv('DB_HOST')
    db_database = os.getenv('DB_DATABASE')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Verifica se todas as credenciais estão definidas corretamente
    if not all([db_host, db_database, db_user, db_password]):
        print("Erro: As credenciais de banco de dados não foram definidas corretamente.")
        return None

    try:
        # Tenta estabelecer a conexão com o banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_user,
            password=db_password
        )

        # Verifica se a conexão foi bem-sucedida
        if connection.is_connected():
            
            return connection
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def close_connection(connection):
    """Close the database connection."""
    # Fecha a conexão se estiver ativa
    if connection and connection.is_connected():
        connection.close()
        print("Conexão com o banco de dados encerrada.")
    else:
        print("A conexão já está encerrada ou inválida.")
