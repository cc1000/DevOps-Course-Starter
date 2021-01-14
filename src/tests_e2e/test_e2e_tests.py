import os
from dotenv import find_dotenv, load_dotenv
from threading import Thread
import pytest
import uuid
from selenium import webdriver
import app
import board_api as board_api

@pytest.fixture(scope='module')
def test_app():
    load_dotenv(find_dotenv('.env'), override=True)

    board_name = f'Corndell_tests_{uuid.uuid4()}'
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

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def test_load_page(test_app, driver):
    driver.get('http://localhost:5000')

    assert driver.title == 'To-Do App'

def test_add_item(test_app, driver):
    driver.get('http://localhost:5000')

    new_item_title = f'New item {uuid.uuid4()}'

    new_item_input = driver.find_element_by_name('title')
    new_item_input.send_keys(new_item_title)

    add_new_item_button = driver.find_element_by_name('add')
    add_new_item_button.click()

    to_do_items_div = driver.find_element_by_id('toDoItems')
    assert new_item_title in to_do_items_div.text

def test_complete_item(test_app, driver):
    driver.get('http://localhost:5000')

    new_item_title = f'New item {uuid.uuid4()}'

    new_item_input = driver.find_element_by_name('title')
    new_item_input.send_keys(new_item_title)

    add_new_item_button = driver.find_element_by_name('add')
    add_new_item_button.click()

    complete_item_links = driver.find_elements_by_name('completeItem') 
    new_item_complete_link = complete_item_links[len(complete_item_links) - 1]
    new_item_complete_link.click()

    to_do_items_div = driver.find_element_by_id('toDoItems')
    assert new_item_title not in to_do_items_div.text

    completed_items_div = driver.find_element_by_id('completedItems')
    assert new_item_title in completed_items_div.text

def test_delete_item(test_app, driver):
    driver.get('http://localhost:5000')

    new_item_title = f'New item {uuid.uuid4()}'

    new_item_input = driver.find_element_by_name('title')
    new_item_input.send_keys(new_item_title)

    add_new_item_button = driver.find_element_by_name('add')
    add_new_item_button.click()

    to_do_items_div = driver.find_element_by_id('toDoItems')
    delete_item_links = to_do_items_div.find_elements_by_name('deleteItem') 
    delete_item_link = delete_item_links[len(delete_item_links) - 1]
    delete_item_link.click()

    all_items_div = driver.find_element_by_id('allItems')
    assert new_item_title not in all_items_div.text