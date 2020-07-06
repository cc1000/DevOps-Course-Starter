import requests
import trello_config
from ToDoItem import ToDoItem

def get_items():
    response = requests.get(f'{trello_config.root_url}/boards/{trello_config.board_id}/cards?key={trello_config.api_key}&token={trello_config.token}')
    response.raise_for_status()
    trello_cards = response.json()
    return [ToDoItem(card) for card in trello_cards]

def add_item(title):
    payload = {
        'key': trello_config.api_key,
        'token': trello_config.token,
        'idList': trello_config.todo_list_id,
        'name': title
    }
    response = requests.post(f'{trello_config.root_url}/cards', data=payload)
    response.raise_for_status()

def complete_item(id):
    payload = {
        'key': trello_config.api_key,
        'token': trello_config.token,
        'idList': trello_config.done_list_id
    }
    response = requests.put(f'{trello_config.root_url}/cards/{id}', data=payload)
    response.raise_for_status()


def delete_item(id):
    response = requests.delete(f'{trello_config.root_url}/cards/{id}?key={trello_config.api_key}&token={trello_config.token}')
    response.raise_for_status()