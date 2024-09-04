import requests
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import datetime

# Carregar as variáveis do arquivo .env
_ = load_dotenv(find_dotenv())

# Configurações do MongoDB
username = os.getenv("MONGO_ADMIN")
password = os.getenv("MONGO_PASSWORD")
mongo_client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/")
db = mongo_client["easy_analytics_db"]
collection = db["kiron_partida"]