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
    data_busca =  datetime.datetime.now() - datetime.timedelta(days=periodo)
    
    # Seleciona no banco o período de partidas
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM matches WHERE match_datetime >= %s", (data_busca,))
    partidas = cursor.fetchall()

    cursor.close()
    conn.close()
    
    # Converter o resultado em JSON
    partidas_json = json.dumps(partidas, default=str)
    return jsonify(json.loads(partidas_json))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=flask_port, debug=True)