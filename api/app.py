from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(os.path.dirname('app.py')), '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

mongo_uri = os.getenv('MONGO_URI')
mongo_name = os.getenv('MONGO_NAME')
flask_port = os.getenv('FLASK_PORT')

# Conectar ao MongoDB
client = MongoClient(mongo_uri)
db = client.mongo_name
collection = db.clients

@app.route('/addClient', methods=['POST'])
def add_client():
    data = request.json
    
    name = data.get('name')
    token = data.get('token')
    affiliate = data.get('affiliate')
    status = data.get('status')
    
    if name and token and affiliate and status is not None:
      response = {
              "name": name,
              "token": token,
              "affiliate": affiliate,
              "status": status
          }
      collection.insert_one(response)
    
      return jsonify({"status": "cliente adicionado"}), 201
    else:
        return jsonify({"error": "dados incompletos"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=flask_port)
