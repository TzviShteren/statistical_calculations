from app.db.mongo_db.connection import get_collection
from dotenv import load_dotenv

load_dotenv(verbose=True)


def insert_event_to_mongo(data):
    try:
        get_collection().insert_many(data)
        print(f"Document inserted")

    except Exception as e:
        print(f"An error occurred: {e}")

