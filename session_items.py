from flask import session
import requests
from trello_config_reader import get_config

trello_root_url = 'https://api.trello.com/1'
trello_board_id = '5ef8f1926a457142f41ac6ed'
trello_todo_list_id = '5ef8f19a64a8ef61948d43fd'
trello_done_list_id = '5ef8f19c4743080e63d5db1c'
trello_api_key = get_config('api_key')
trello_token = get_config('token')

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    response = requests.get(f'{trello_root_url}/boards/{trello_board_id}/cards?key={trello_api_key}&token={trello_token}')
    response.raise_for_status()
    return response.json()


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
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


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def remove_item(id):
    existing_items = get_items()
    updated_items = list(filter(lambda x: x['id'] != id, existing_items))

    session['items'] = updated_items