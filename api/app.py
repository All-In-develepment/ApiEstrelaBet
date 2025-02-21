from flask import Flask, request, jsonify
import datetime
import os
import json
from bson import ObjectId
from dotenv import load_dotenv, find_dotenv
import mysql.connector

app = Flask(__name__)

# Carregar as variáveis do arquivo .env
_ = load_dotenv(find_dotenv())

flask_port = os.getenv('FLASK_PORT')   # Porta do Flask

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

# Função personalizada para converter ObjectId em string
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

# Usando a classe JSONEncoder personalizada globalmente (opcional)
app.json_encoder = JSONEncoder

def custom_json_converter(obj):
    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()  # Ou use obj.days, dependendo do que for mais útil para você
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@app.route('/api/partidas', methods=['GET'])
def get_partidas():
    periodo = request.args.get('periodo', default=7, type=int)
    data_busca =  datetime.datetime.now() - datetime.timedelta(hours=periodo)
    data_inicial_busca = datetime.datetime(data_busca.year, data_busca.month, data_busca.day, data_busca.hour, 0, 0)
    
    # Seleciona no banco o período de partidas
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    print(datetime.datetime.strftime(data_inicial_busca, '%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    cursor.execute("SELECT * FROM matches WHERE match_datetime BETWEEN %s AND %s ORDER BY match_datetime DESC", (data_inicial_busca, datetime.datetime.now(),))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

@app.route('/api/partidas/<team_a>/<team_b>/<quant>', methods=['GET'])
def get_partidas_by_team_a_and_team_b(team_a, team_b, quant):
    periodo = request.args.get('periodo', default=7, type=int)
    data_busca =  datetime.datetime.now() - datetime.timedelta(hours=periodo)
    data_inicial_busca = datetime.datetime(data_busca.year, data_busca.month, data_busca.day, data_busca.hour, 0, 0)
    
    # Seleciona no banco o período de partidas
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    print(datetime.datetime.strftime(data_inicial_busca, '%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    cursor.execute("SELECT * FROM matches WHERE (team_home = %s OR team_visitor = %s) AND (team_home = %s OR team_visitor = %s) ORDER BY match_datetime DESC LIMIT %s", (team_a, team_a, team_b, team_b, int(quant)))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

@app.route('/api/jogos365', methods=['GET'])
def get_jogos365():
    periodo = request.args.get('periodo', default=7, type=int)
    data_busca =  datetime.datetime.now() - datetime.timedelta(hours=periodo)
    data_inicial_busca = datetime.datetime(data_busca.year, data_busca.month, data_busca.day, data_busca.hour, 0, 0)
    
    # Seleciona no banco o período de partidas
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Partida WHERE DateTimeInserte BETWEEN %s AND %s ORDER BY DateTimeInserte DESC", (data_inicial_busca, datetime.datetime.now(),))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

# Rota para buscar partidas de um time específico
@app.route('/api/jogos365/<team_a>/<team_b>/<quant>', methods=['GET'])
def get_jogos_bet365_by_team_a_and_team_b(team_a, team_b, quant):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Partida WHERE (TimeA = %s OR TimeB = %s) AND (TimeA = %s OR TimeB = %s) ORDER BY DateTimeInserte DESC LIMIT %s", (team_a, team_a, team_b, team_b, int(quant)))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    for partida in partidas:
        partida['team_home_name '] = partida['TimeA']
        partida['team_visitor_name '] = partida['TimeB']
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

@app.route('/api/jogos365byteam/<team_a>/<quant>', methods=['GET'])
def get_jogos_bet365_by_team_a(team_a, quant):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Partida WHERE TimeA = %s OR TimeB = %s ORDER BY DateTimeInserte DESC LIMIT %s", (team_a, team_a, int(quant)))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    for partida in partidas:
        partida['team_home_name '] = partida['TimeA']
        partida['team_visitor_name '] = partida['TimeB']
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=flask_port, debug=True)