import os
import requests
from to_do_item import ToDoItem

root_url = os.environ['TRELLO_ROOT_URL']
api_key = os.environ['TRELLO_API_KEY']
token = os.environ['TRELLO_TOKEN']
board_name = os.environ['TRELLO_BOARD_NAME']

def get_items():
    params = {
        'key': api_key,
        'token': token
    }
    done_list_id = get_list_id('Done')

    response = requests.get(f'{root_url}/boards/{get_board_id()}/cards', params=params)
    response.raise_for_status()
    trello_cards = response.json()
    return [ToDoItem.from_trello_data(card, done_list_id) for card in trello_cards]

def add_item(title):
    payload = {
        'key': api_key,
        'token': token,
        'idList': get_list_id('ToDo'),
        'name': title
    }
    response = requests.post(f'{root_url}/cards', data=payload)
    response.raise_for_status()

def complete_item(id):
    payload = {
        'key': api_key,
        'token': token,
        'idList': get_list_id('Done')
    }
    response = requests.put(f'{root_url}/cards/{id}', data=payload)
    response.raise_for_status()

def delete_item(id):
    api_key = api_key
    token = token
    response = requests.delete(f'{root_url}/cards/{id}?key={api_key}&token={token}')
    response.raise_for_status()

def get_list_id(list_name):
    params = {
        'key': api_key,
        'token': token
    }

    response = requests.get(f'{root_url}/boards/{get_board_id()}/lists', params=params)
    response.raise_for_status()
    
    return list(filter(lambda list: list['name'] == list_name, response.json()))[0]['id']

def get_board_id():
    params = {
        'key': api_key,
        'token': token
    }

    response = requests.get(f'{root_url}/members/me/boards', params=params)
    response.raise_for_status()

    return list(filter(lambda board: board['name'] == board_name, response.json()))[0]['id']