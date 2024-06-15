from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

user = os.getenv("MONGODB_LOGIN")
password = os.getenv("MONGODB_PASSWORD")
endpoint = os.getenv("MONGODB_ENDPOINT")

uri = f"mongodb+srv://{user}:{password}@{endpoint}/?retryWrites=true&w=majority&appName=FIAP"
cluster = MongoClient(uri, server_api=ServerApi('1'))

mongo_db = cluster["database"]
collections = mongo_db["intel_db"]


def insert(user_id, data):
    query = dict(id=user_id)
    update = dict(id=user_id, secret=data)
    collections.replace_one(query, update, True)


def get(user_id):
    return collections.find_one({"id": str(user_id)})
