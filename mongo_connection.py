from pymongo import MongoClient

# Função para conectar ao MongoDB
def conectar_mongo():
    # Conectar ao MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mongodb']  # Nome do banco de dados
    return db

# Função para inserir dados no MongoDB
def inserir_dados_no_mongo(db, game_id, game_teams, resultado):
    collection = db['partidas']  # Nome da coleção

    # Estrutura dos dados a serem inseridos
    game_data = {
        'id_partida': game_id,
        'times_que_jogaram': game_teams,
        'resultado': resultado
    }

    # Inserir os dados na coleção
    collection.insert_one(game_data)

    print(f"Dados da partida {game_id} inseridos no MongoDB com sucesso!")
