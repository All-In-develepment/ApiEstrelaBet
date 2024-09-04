# from api.db_connector__ import MongoDBConnector
import mysql.connector
import os
import requests
from dotenv import load_dotenv, find_dotenv
import time
import datetime

# Carregar as variáveis do arquivo .env
_ = load_dotenv(find_dotenv())

## Configuração do banco de dados MySQL
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    # 'host': 'localhost',  # Este é o nome do serviço no Docker Compose
    'host': 'mysql_db',  # Este é o nome do serviço no Docker Compose
    'database': os.getenv('MYSQL_DATABASE')
}

# Conexão com o banco de dados
def connect_db():
    return mysql.connector.connect(**db_config)

def Populador():
    # {'league': 'EnglishFastLeagueFootballSingleMatch', 'hour_match': '12:28', 'data_match': '04/09/2024', 'team_home': 'LEI', 'team_visitor': 'TOT', 'scoreboard': '2 x 2', 'hora': 12, 'minuto': 28}
    if __name__ == "__main__":
        # URL da API
        url = "https://www.plataforma.easycoanalytics.com.br/api-easy-analytics/api.php?action=getKironPartida"

        # Fazer a requisição para a API
        response = requests.get(url).json()

        conn = connect_db()
        cursor = conn.cursor()

        # Critérios de busca
        for partida in response['retorno'][0:3]:
            partida['match_datetime'] = datetime.datetime(int(partida['data_match'].split('/')[2]), int(partida['data_match'].split('/')[1]), int(partida['data_match'].split('/')[0]), int(partida['hora']), int(partida['minuto']))
            query_select = f"""SELECT * FROM matches WHERE league = "{partida['league']}" AND match_datetime = "{partida['match_datetime']}" AND team_home = "{partida['team_home']}" AND team_visitor = "{partida['team_visitor']}" """
            cursor.execute(query_select)
            result = cursor.fetchone()
            if result == None:
                query_insert = f"""
                    INSERT INTO matches (`league`, `hour_match`, `date_match`, `match_datetime`, `team_home`, `team_visitor`, `scoreboard`, `hora`, `minuto`) 
                    VALUES ("{partida['league']}", "{partida['hour_match']}", "{partida['data_match']}", "{partida['match_datetime']}", "{partida['team_home']}", "{partida['team_visitor']}", "{partida['scoreboard']}", "{partida['hora']}", "{partida['minuto']}")"""
                cursor.execute(query_insert)
                conn.commit()
                print('Partida inserida com sucesso')

        cursor.close()
        conn.close()

while True:
    Populador()
    time.sleep(60)
