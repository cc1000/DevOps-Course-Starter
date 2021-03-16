import os
from to_do_item import ToDoItem
from pymongo import MongoClient
from datetime import datetime

mongo_uri = os.environ['MONGO_URI']
mongo_username = os.environ['MONGO_USERNAME']
mongo_password = os.environ['MONGO_PASSWORD']
mongo_db_name = os.environ['MONGO_DB_NAME']

mongoClient = MongoClient(f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_uri}/?w=majority')
db = mongoClient[mongo_db_name]
itemsCollection = db.items

def get_items():
    items = itemsCollection.find()
    return [ToDoItem(item['_id'], item['name'], item['status'], item['lastModified']) for item in items]

def add_item(title):
    itemsCollection.insert_one({
        "name": title,
        "status": "To Do",
        "lastModified": datetime.now()
    })

def complete_item(id):
    payload = {
        'key': get_api_key(),
        'token': get_token(),
        'idList': get_list_id('Done')
    }
    response = requests.put(f'{get_root_url()}/cards/{id}', data=payload)
    response.raise_for_status()

def delete_item(id):
    api_key = get_api_key()
    token = get_token()
    response = requests.delete(f'{get_root_url()}/cards/{id}?key={api_key}&token={token}')
    response.raise_for_status()

def delete_board(id):
    api_key = get_api_key()
    token = get_token()
    response = requests.delete(f'{get_root_url()}/boards/{id}?key={api_key}&token={token}')
    response.raise_for_status()