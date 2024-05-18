from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://fiap:paifxpto@fiap.zfhhiqb.mongodb.net/?retryWrites=true&w=majority&appName=fiap"
cluster = MongoClient(uri, server_api=ServerApi('1'))

mongo_db = cluster["database"]
hashes_collections = mongo_db["hashes"]


def insert(data):
    entity = dict(hash=data)
    hashes_collections.insert_one(entity)


def get(hash):
    return hashes_collections.find_one({"hash": str(hash)})