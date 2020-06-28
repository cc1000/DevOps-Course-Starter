from flask import session
import requests
from trello_config_reader import get_config

trello_root_url = 'https://api.trello.com/1'
trello_board_id = '5ef8f1926a457142f41ac6ed'
trello_todo_list_id = '5ef8f19a64a8ef61948d43fd'
trello_done_list_id = '5ef8f19c4743080e63d5db1c'
trello_api_key = get_config('api_key')
trello_token = get_config('token')

def get_items():
    response = requests.get(f'{trello_root_url}/boards/{trello_board_id}/cards?key={trello_api_key}&token={trello_token}')
    response.raise_for_status()
    return response.json()

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