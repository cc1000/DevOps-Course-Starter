import pytest
from dotenv import find_dotenv, load_dotenv
import requests
import app
from board_repository import BoardRepository
from to_do_item import ToDoItem
from datetime import datetime
from auth_provider import AuthProvider
from app_user import AppUser
from flask_login import current_user

@pytest.fixture
def client():
    load_dotenv(find_dotenv('.env.test'), override=True)

    def mock_init(self): pass
    BoardRepository.__init__ = mock_init

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):  
    monkeypatch.setattr(
        'board_repository.BoardRepository.get_items', 
        lambda self: [
            ToDoItem('123', 'Wash the car', 'To Do', datetime.now()),
            ToDoItem('456', 'Fly to space', 'Completed', datetime.now())
        ]
    )

    mock_user(monkeypatch, client, roles=[AuthProvider.READER_ROLE])

    response = client.get('/')

    assert response.status_code == 200

    response_body = response.get_data(True)
    assert 'Wash the car' in response_body
    assert 'Fly to space' in response_body

def test_index_page_returns_403_if_user_not_in_reader_role(monkeypatch, client):
    mock_user(monkeypatch, client, roles=[AuthProvider.WRITER_ROLE])

    response = client.get('/')

    assert response.status_code == 403

def mock_user(monkeypatch, client, roles):
    user = AppUser('someUserId', roles)

    monkeypatch.setattr('auth_provider.AuthProvider.get_authenticated_user', lambda self, auth_code: user)
    monkeypatch.setattr('auth_provider.AuthProvider.get_user', lambda self, user_id: user)

    client.get('/login/callback?code=someUserId')