from flask import session
import requests
from trello_config import trello_api_key, trello_token, trello_root_url, trello_board_id, trello_todo_list_id, trello_done_list_id
from ToDoItem import ToDoItem

def get_items():
    response = requests.get(f'{trello_root_url}/boards/{trello_board_id}/cards?key={trello_api_key}&token={trello_token}')
    response.raise_for_status()
    trello_cards = response.json()
    return [ToDoItem(card) for card in trello_cards]

def add_item(title):
    payload = {
        'key': trello_api_key,
        'token': trello_token,
        'idList': trello_todo_list_id,
        'name': title
    }
    response = requests.post(f'{trello_root_url}/cards', data=payload)
    response.raise_for_status()

def complete_item(id):
    payload = {
        'key': trello_api_key,
        'token': trello_token,
        'idList': trello_done_list_id
    }
    response = requests.put(f'{trello_root_url}/cards/{id}', data=payload)
    response.raise_for_status()


def delete_item(id):
    response = requests.delete(f'{trello_root_url}/cards/{id}?key={trello_api_key}&token={trello_token}')
    response.raise_for_status()