from flask import Flask, jsonify, request
from threading import Thread
from datetime import time
from mongo_connection import conectar_mongo
from dudu_rapaspadinha3 import main as start_scraping_task, stop_scraping_task

app = Flask(__name__)

# Conectar ao MongoDB
db = conectar_mongo()

scraping_thread = None
scraping_active = False

@app.route('/api/partidas', methods=['GET'])
def get_partidas():
    partidas = db['partidas'].find()
    result = []
    for partida in partidas:
        result.append({
            'id_partida': partida['id_partida'],
            'times_que_jogaram': partida['times_que_jogaram'],
            'resultado': partida['resultado']
        })
    return jsonify(result)

@app.route('/api/partidas', methods=['POST'])
def add_partida():
    data = request.get_json()
    partida = {
        'id_partida': data['id_partida'],
        'times_que_jogaram': data['times_que_jogaram'],
        'resultado': data['resultado']
    }
    db['partidas'].insert_one(partida)
    return jsonify({'msg': 'Partida adicionada com sucesso!'}), 201

@app.route('/scraping/start', methods=['POST'])
def start_scraping():
    global scraping_thread, scraping_active
    if scraping_active:
        return jsonify({"message": "Scraping já está em execução."}), 400

    data = request.get_json()
    interval = data.get('interval', 60)  # Pega o intervalo do corpo da requisição, ou usa 60 segundos como padrão

    scraping_active = True
    scraping_thread = Thread(target=start_scraping_task, args=(interval,))
    scraping_thread.start()
    return jsonify({"message": "Scraping iniciado", "interval": interval})

@app.route('/scraping/stop', methods=['POST'])
def stop_scraping():
    global scraping_active
    if not scraping_active:
        return jsonify({"message": "Scraping não está em execução."}), 400

    stop_scraping_task()  # Função para parar o scraping
    scraping_active = False
    return jsonify({"message": "Scraping parado"})


if __name__ == '__main__':
    app.run(debug=True)
