import os
from threading import Thread
import pytest
import app
import board_api as board_api

@pytest.fixture(scope='module')
def test_app():
    board_name = 'Corndell_tests'
    board_id = board_api.create_board(board_name)
    os.environ['TRELLO_BOARD_NAME'] = board_name

    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    yield app

    # Tear Down
    thread.join(1)
    board_api.delete_board(board_id)

def test_thing(test_app):
    x = 1