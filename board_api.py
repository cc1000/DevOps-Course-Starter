import requests
import trello_config
from to_do_item import ToDoItem

def get_items():
    params = {
        'key': trello_config.api_key,
        'token': trello_config.token
    }
    done_list_id = get_list_id('Done')

    response = requests.get(f'{trello_config.root_url}/boards/{get_board_id()}/cards', params=params)
    response.raise_for_status()
    trello_cards = response.json()
    return [ToDoItem(card, done_list_id) for card in trello_cards]

def add_item(title):
    payload = {
        'key': trello_config.api_key,
        'token': trello_config.token,
        'idList': get_list_id('ToDo'),
        'name': title
    }
    response = requests.post(f'{trello_config.root_url}/cards', data=payload)
    response.raise_for_status()

def complete_item(id):
    payload = {
        'key': trello_config.api_key,
        'token': trello_config.token,
        'idList': get_list_id('Done')
    }
    response = requests.put(f'{trello_config.root_url}/cards/{id}', data=payload)
    response.raise_for_status()

def delete_item(id):
    response = requests.delete(f'{trello_config.root_url}/cards/{id}?key={trello_config.api_key}&token={trello_config.token}')
    response.raise_for_status()

def get_list_id(list_name):
    params = {
        'key': trello_config.api_key,
        'token': trello_config.token
    }

    response = requests.get(f'{trello_config.root_url}/boards/{get_board_id()}/lists', params=params)
    response.raise_for_status()
    
    return list(filter(lambda list: list['name'] == list_name, response.json()))[0]['id']

def get_board_id():
    params = {
        'key': trello_config.api_key,
        'token': trello_config.token
    }

    response = requests.get(f'{trello_config.root_url}/members/me/boards', params=params)
    response.raise_for_status()

    return list(filter(lambda board: board['name'] == 'Corndell', response.json()))[0]['id']