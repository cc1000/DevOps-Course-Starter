import os
import requests
from to_do_item import ToDoItem

def get_root_url(): return os.environ['TRELLO_ROOT_URL']
def get_api_key(): return os.environ['TRELLO_API_KEY']
def get_token(): return os.environ['TRELLO_TOKEN']
def get_board_name(): return os.environ['TRELLO_BOARD_NAME']

def get_items():
    params = {
        'key': get_api_key(),
        'token': get_token()
    }
    done_list_id = get_list_id('Done')

    response = requests.get(f'{get_root_url()}/boards/{get_board_id()}/cards', params=params)
    response.raise_for_status()
    trello_cards = response.json()
    return [ToDoItem.from_trello_data(card, done_list_id) for card in trello_cards]

def add_item(title):
    payload = {
        'key': get_api_key(),
        'token': get_token(),
        'idList': get_list_id('To Do'),
        'name': title
    }
    response = requests.post(f'{get_root_url()}/cards', data=payload)
    response.raise_for_status()

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

def get_list_id(list_name):
    params = {
        'key': get_api_key(),
        'token': get_token()
    }

    response = requests.get(f'{get_root_url()}/boards/{get_board_id()}/lists', params=params)
    response.raise_for_status()
    
    return list(filter(lambda list: list['name'] == list_name, response.json()))[0]['id']

def get_board_id():
    params = {
        'key': get_api_key(),
        'token': get_token()
    }

    response = requests.get(f'{get_root_url()}/members/me/boards', params=params)
    response.raise_for_status()

    return list(filter(lambda board: board['name'] == get_board_name(), response.json()))[0]['id']

def create_board(name):
    payload = {
        'key': get_api_key(),
        'token': get_token(),
        'name': name
    }
    response = requests.post(f'{get_root_url()}/boards', data=payload)
    response.raise_for_status()

    board_id = response.json()['id']
    return board_id

def delete_board(id):
    api_key = get_api_key()
    token = get_token()
    response = requests.delete(f'{get_root_url()}/boards/{id}?key={api_key}&token={token}')
    response.raise_for_status()