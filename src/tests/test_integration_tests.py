import pytest
from dotenv import find_dotenv, load_dotenv
import requests
import app

@pytest.fixture
def client():
    load_dotenv(find_dotenv('.env.test'), override=True)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    board_id = 'board_1'
    to_do_list_id = 'to_do_list_id'
    completed_list_id = 'completed_list_id'

    def mock_get(url, params):
        if '/members/me/boards' in url:
            return MockResponse([
                get_board(board_id, 'Test board'),
                get_board('another_id', 'Another board')
            ])
        if f'/boards/{board_id}/lists' in url:
            return MockResponse([
                get_list(to_do_list_id, 'To Do'),
                get_list(completed_list_id, 'Done')
            ])            
        elif f'/boards/{board_id}/cards' in url:
            return MockResponse([
                get_board_item('123', 'Wash the car', to_do_list_id, '2020-07-30T20:17:50.227Z'),
                get_board_item('123', 'Fly to space', completed_list_id, '2020-07-28T06:18:12.008Z')
            ])
    
    monkeypatch.setattr('requests.get', mock_get)

    response = client.get('/')

    assert response.status_code == 200

    response_body = response.get_data(True)
    assert 'Wash the car' in response_body
    assert 'Fly to space' in response_body

class MockResponse:
    def __init__(self, responseJson):
        self.responseJson = responseJson

    def raise_for_status(self): return None
    def json(self): return self.responseJson

def get_board(id, name):
    return {
        'name': name,
        'desc': '',
        'descData': None,
        'closed': False,
        'idOrganization': None,
        'idEnterprise': None,
        'limits': None,
        'pinned': None,
        'shortLink': 'Pz4qi9vp',
        'powerUps': [],
        'dateLastActivity': '2019-12-02T20:24:39.835Z',
        'idTags': [],
        'datePluginDisable': None,
        'creationMethod': None,
        'ixUpdate': None,
        'enterpriseOwned': False,
        'idBoardSource': None,
        'id': id,
        'starred': True,
        'url': 'https://trello.com/b/Pz4qi9vp/xmas',
        'subscribed': True,
        'dateLastView': '2019-12-02T20:29:40.138Z',
        'shortUrl': 'https://trello.com/b/Pz4qi9vp',
        'templateGallery': None,
        'premiumFeatures': []
    }

def get_list(id, name):
    return {
        'id': id,
        'name': name,
        'closed': False,
        'pos': 65535,
        'softLimit': None,
        'idBoard': '5ef8f1926a457142f41ac6ed',
        'subscribed': False
    }

def get_board_item(id, name, id_list, last_updated):
    return {
        'id': id,
        'checkItemStates': None,
        'closed': False,
        'dateLastActivity': last_updated,
        'desc': '',
        'descData': None,
        'dueReminder': None,
        'idBoard': 'board_1',
        'idList': id_list,
        'idMembersVoted': [],
        'idShort': 13,
        'idAttachmentCover': None,
        'idLabels': [],
        'manualCoverAttachment': False,
        'name': name,
        'pos': 98304,
        'shortLink': 'lOvZ1dFX',
        'isTemplate': False,
        'dueComplete': False,
        'due': None,
        'idChecklists': [],
        'idMembers': [],
        'labels': [],
        'shortUrl': 'https://trello.com/c/lOvZ1dFX',
        'subscribed': False,
        'url': 'https://trello.com/c/lOvZ1dFX/13-new-3'
    }