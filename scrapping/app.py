from flask import Flask, jsonify
from mongo_connection_v2 import conectar_mongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()


flask_port = os.getenv('FLASK_PORT')
mongo_uri = os.getenv('MONGO_URI')
mongo_name = os.getenv('MONGO_NAME')
mongo_col = os.getenv('MONGO_COLLECTION')

# Conectar ao MongoDB
client= MongoClient(mongo_uri)
db = client[mongo_name]  # Usar a variável de ambiente para acessar o banco de dados
collection = db[mongo_col]
# collection=db.mongo_col
@app.route('/api/partidas', methods=['GET'])
def get_partidas():
    partidas = collection.find()
    arr = list(partidas)
    print(arr)
    result = []
    for partida in arr:
        print(partida)
        result.append({
            'id_partida': partida.get('id_partida'),
            'times_que_jogaram': partida.get('times_que_jogaram'),
            'resultado': partida.get('resultado'),
            'data_e_hora_atual': partida.get('data_e_hora_atual'),
            'data_e_hora_4_min_antes': partida.get('data_e_hora_4_min_antes'),
            'data_e_hora_2_min_antes': partida.get('data_e_hora_2_min_antes')
        })
    return jsonify(result)
@app.route('/', methods=['GET'])  
def hello_world():
    return 'funcionou2'
@app.route('/api/status', methods=['GET'])
def status():
    try:
        # Verifica a conexão com o MongoDB
        db.command("ping")
        return jsonify({"status": "success", "message": "MongoDB is connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=flask_port, debug=True)