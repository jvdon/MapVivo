from pymongo import MongoClient
from pymongo.collection import Collection
from bson import json_util
import json
import threading
from conf import mongodb_uri

"""obj = {
    user_id: number,
    in_cache: bool,
    last_seen: date
}
"""

cache_lock = threading.Lock()


def open_db() -> Collection:
    with cache_lock:
        try:
            # Create a MongoClient instance
            client = MongoClient(mongodb_uri)

            # Check connection
            server_info = (
                client.server_info()
            )  # This will raise an exception if unable to connect
            print("[UPDATABLE] Connected to MongoDB cluster.")

            # Access the 'test' database
            db = client.MapVIVO
            return db.get_collection("updatable")
        except ConnectionError as e:
            print(f"[UPDATABLE] Error connecting to MongoDB: {e}")
            return None


# Read All
def getAll():
    updatable = open_db()
    if updatable is None:
        return [], False
    try:
        return (
            json.loads(json_util.dumps([document for document in updatable.find({})])),
            True,
        )
    except Exception as e:
        print(f"Error reading all entries: {e}")
        return [], False


# Read
def get(cliente: str):
    updatable = open_db()
    if updatable is None:
        return [], False
    try:
        return (
            json.loads(
                json_util.dumps(
                    [document for document in updatable.find({"user_id": cliente})]
                )
            ),
            True,
        )
    except Exception as e:
        print(f"Error reading all entries: {e}")
        return [], False


# Write


def save(content):
    updatable = open_db()
    if updatable is None:
        return False
    try:
        updatable.insert_one(content)
        return True
    except:
        return False


# Update


def update(user_id: str, content):
    updatable = open_db()
    if updatable is None:
        return False
    try:
        updatable.replace_one({"user_id": user_id}, content)
        return True
    except Exception as e:
        print(e)
        return False


# Delete
def delete(user_id):
    updatable = open_db()
    if updatable is None:
        return False
    try:
        updatable.delete_one(filter={"user_id": user_id})
        return True
    except:
        return False


def usage():
    return -1