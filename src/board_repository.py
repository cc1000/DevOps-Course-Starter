import os
from to_do_item import ToDoItem
from pymongo import MongoClient
from bson import ObjectId
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
    return [ToDoItem(str(item['_id']), item['name'], item['status'], item['lastModified']) for item in items]

def add_item(title):
    itemsCollection.insert_one({
        'name': title,
        'status': 'To Do',
        'lastModified': datetime.now()
    })

def complete_item(id):
    itemsCollection.update_one(
        {'_id': ObjectId(id)}, 
        {'$set': {'status': 'Done'}}
    )

def delete_item(id):
    itemsCollection.delete_one({'_id': ObjectId(id)})