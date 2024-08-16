from flask import Flask, jsonify, request
from mongo_connection import conectar_mongo

app = Flask(__name__)

# Conectar ao MongoDB
db = conectar_mongo()

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

if __name__ == '__main__':
    app.run(debug=True)
