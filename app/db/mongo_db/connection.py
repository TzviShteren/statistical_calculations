from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


def get_client():
    return MongoClient(os.environ['MONGO_URL'])


def get_collection():
    db = get_client()['terrorism_data']
    return db['events']
