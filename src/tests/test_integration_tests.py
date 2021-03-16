import pytest
from dotenv import find_dotenv, load_dotenv
import requests
import app
import board_repository
from to_do_item import ToDoItem
from datetime import datetime

@pytest.fixture
def client():
    load_dotenv(find_dotenv('.env.test'), override=True)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    def mock_get_items():
        return [
            ToDoItem('123', 'Wash the car', 'To Do', datetime.now()),
            ToDoItem('456', 'Fly to space', 'Completed', datetime.now())
        ]
    
    monkeypatch.setattr('board_repository.get_items', mock_get_items)

    response = client.get('/')

    assert response.status_code == 200

    response_body = response.get_data(True)
    assert 'Wash the car' in response_body
    assert 'Fly to space' in response_body