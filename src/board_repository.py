import os
from to_do_item import ToDoItem
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

class BoardRepository:
    def __init__(self):
        self.mongoClient = MongoClient(os.environ['MONGO_CONNECTION_STRING'])
        self.db = self.mongoClient[os.environ['MONGO_DB_NAME']]
        self.itemsCollection = self.db.items

    def get_items(self):
        items = self.itemsCollection.find()
        return [ToDoItem(str(item['_id']), item['name'], item['status'], item['lastModified']) for item in items]

    def add_item(self, title):
        self.itemsCollection.insert_one({
            'name': title,
            'status': 'To Do',
            'lastModified': datetime.now()
        })

    def complete_item(self, id):
        self.itemsCollection.update_one(
            {'_id': ObjectId(id)}, 
            {'$set': {'status': 'Completed'}}
        )

    def delete_item(self, id):
        self.itemsCollection.delete_one({'_id': ObjectId(id)})

    def delete_db(self):
        self.mongoClient.drop_database(self.db.name)