import pytest
from datetime import datetime, timedelta
from to_do_items_view_model import ToDoItemsViewModel
from to_do_item import ToDoItem
from app_user import AppUser
from auth_provider import AuthProvider

items = [
    ToDoItem('id_1', 'To do 1', ToDoItem.to_do_status, datetime.now()),
    ToDoItem('id_2', 'To do 2', ToDoItem.to_do_status, datetime.now()),
    ToDoItem('id_3', 'Completed 1', ToDoItem.completed_status, datetime.now())
]

@pytest.fixture
def view_model() -> ToDoItemsViewModel:
    return ToDoItemsViewModel(user_roles=[], items=items)

def test_user_is_writer_is_false_if_user_is_not_in_writer_role():
    view_model = ToDoItemsViewModel(user_roles=[AuthProvider.READER_ROLE], items=[])
    assert view_model.user_is_writer == False

def test_user_is_writer_is_true_if_user_is_in_writer_role():
    view_model = ToDoItemsViewModel(user_roles=[AuthProvider.WRITER_ROLE], items=[])
    assert view_model.user_is_writer == True

def test_can_get_all_items(view_model):
    assert view_model.all_items == items

def test_can_get_all_items_in_status_to_do(view_model):
    items = view_model.to_do_items
    assert len(items) == 2
    assert items[0].id == 'id_1'
    assert items[1].id == 'id_2'

def test_can_get_all_items_in_status_completed(view_model):
    items = view_model.completed_items
    assert len(items) == 1
    assert items[0].id == 'id_3'

def test_all_completed_items_shown_if_fewer_than_five():
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    view_model = ToDoItemsViewModel(
        user_roles=[],
        items=[
            ToDoItem('id_1', 'To do 1', ToDoItem.to_do_status, now),
            ToDoItem('id_2', 'Completed 1', ToDoItem.completed_status, now),
            ToDoItem('id_3', 'Completed 2', ToDoItem.completed_status, now),
            ToDoItem('id_4', 'Completed 3', ToDoItem.completed_status, now),
            ToDoItem('id_5', 'Completed 4', ToDoItem.completed_status, yesterday)
        ]
    )
    
    assert len(view_model.completed_items) == 4
    assert view_model.show_all_completed_items == True
    assert view_model.recent_completed_items == None
    assert view_model.older_completed_items == None

def test_only_completed_items_completed_today_shown_if_more_than_4():
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    view_model = ToDoItemsViewModel(
        user_roles=[],
        items=[
            ToDoItem('id_1', 'To do 1', ToDoItem.to_do_status, now),
            ToDoItem('id_2', 'Completed 1', ToDoItem.completed_status, now),
            ToDoItem('id_3', 'Completed 2', ToDoItem.completed_status, yesterday),
            ToDoItem('id_4', 'Completed 3', ToDoItem.completed_status, now),
            ToDoItem('id_5', 'Completed 4', ToDoItem.completed_status, now),
            ToDoItem('id_6', 'Completed 5', ToDoItem.completed_status, yesterday)
        ]
    )
    
    assert len(view_model.completed_items) == 5
    assert view_model.show_all_completed_items == False

    assert len(view_model.recent_completed_items) == 3
    assert(view_model.recent_completed_items[0]).id == 'id_2'
    assert(view_model.recent_completed_items[1]).id == 'id_4'
    assert(view_model.recent_completed_items[2]).id == 'id_5'

    items = len(view_model.older_completed_items) == 2
    assert(view_model.older_completed_items[0]).id == 'id_3'
    assert(view_model.older_completed_items[1]).id == 'id_6'