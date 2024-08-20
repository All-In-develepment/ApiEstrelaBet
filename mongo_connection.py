from pymongo import MongoClient

def conectar_mongo():
    client = MongoClient('mongodb://admin:MyMongoL0ideDB!!@201.76.43.147:27017/mongodb?authSource=admin')
    db = client['mongodb']
    return db

def inserir_dados_no_mongo(db, game_id, game_teams, resultados, data_e_hora_atual, data_e_hora_4_min_antes, data_e_hora_2_min_antes):
    collection = db['partidas']

    game_data = {
        'id_partida': game_id,
        'times_que_jogaram': game_teams,
        'resultado': resultados,
        'data_e_hora_atual': data_e_hora_atual,
        'data_e_hora_4_min_antes': data_e_hora_4_min_antes,
        'data_e_hora_2_min_antes': data_e_hora_2_min_antes
    }

    # Verificar se o documento já existe para atualização
    existing_document = collection.find_one({'id_partida': game_id})
    if existing_document:
        collection.update_one({'id_partida': game_id}, {'$set': game_data})
    else:
        collection.insert_one(game_data)

    print(f"Dados da partida {game_id} inseridos no MongoDB com sucesso!")
