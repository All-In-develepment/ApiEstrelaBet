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
            
            else:
                print('Partida já existe no banco de dados')

        cursor.close()
        conn.close()

def PapuladorBet365():
	if __name__ == "__main__":
		for league in range(1, 6):
			url=f"https://bet365botwebapi20231115194435.azurewebsites.net/api/futebolvirtual?liga={league}&futuro=true&Horas=Horas3&tipoOdd=&dadosAlteracao=&filtros=&confrontos=false&hrsConfrontos=3"
			header = {
				'Authorization': os.getenv('TOKEN_BB_TIPS')
			}
			
			resposta_bb_tips = requests.get(url, headers=header)
			
			# varifica se a resposta é 200
			if resposta_bb_tips.status_code == 200:
				conn = connect_db()
				cursor = conn.cursor()
				json_response = resposta_bb_tips.json()
				try:
					for linha in json_response['Linhas']:
						for coluna in linha['Colunas']:
							query_select = f"""SELECT * FROM Partida WHERE Id = "{coluna['Id']}" """
							cursor.execute(query_select)
							result = cursor.fetchone()

							# pega a data de hoje coloca em uma variavel com a colunoa de hora e minuto
							DateTimeInserte = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + coluna['Hora'] + ':' + coluna['Minuto']
							
							if result == None:
								try:
									query_insert = f"""INSERT INTO `Partida` (`Id`, `Horario`, `Hora`, `Minuto`, `SiglaA`, `SiglaB`, `TimeA`, `TimeB`, `Resultado`, `Resultado_FT`, `Resultado_HT`, `PrimeiroMarcar`, `UltimoMarcar`, `Vencedor_HT_FT`, `Resultado_HT_Odd`, `DateTimeInserte`) 
	VALUES ("{coluna['Id']}", "{coluna['Horario']}", "{coluna['Hora']}", "{coluna['Minuto']}", "{coluna['SiglaA']}", "{coluna['SiglaB']}", "{coluna['TimeA']}", "{coluna['TimeB']}", "{coluna['Resultado']}", "{coluna['Resultado_FT']}", "{coluna['Resultado_HT']}", "{coluna['PrimeiroMarcar']}", "{coluna['UltimoMarcar']}", "{coluna['Vencedor_HT_FT']}", "{coluna['Resultado_HT_Odd']}", "{DateTimeInserte}")"""
									
									print(query_insert)
									cursor.execute(query_insert)
									conn.commit()
									print('Partida inserida com sucesso')
								except Exception as e:
									print (f"Erro ao inserir partida: {e}")
									continue
							else:
								print("Parida encontrada")
				except Exception as e:
					print (f"Deu um erro ai: {e}")
			else:
				print('Erro ao buscar partidas')

while True:
    # Populador()
    Populador()
    time.sleep(60)
