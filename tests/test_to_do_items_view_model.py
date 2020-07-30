import pytest
#from new_thing import NewThing
from to_do_items_view_model import ToDoItemsViewModel
from to_do_item import ToDoItem

items = [
    ToDoItem('id_1', 'To do 1', ToDoItem.to_do_status),
    ToDoItem('id_2', 'To do 2', ToDoItem.to_do_status),
    ToDoItem('id_3', 'Completed 1', ToDoItem.completed_status),
]

@pytest.fixture
def view_model() -> ToDoItemsViewModel:
    return ToDoItemsViewModel(items)

def test_can_get_all_items(view_model):
    assert view_model.all_items == items

def test_can_get_all_items_in_status_to_do(view_model):
    items = view_model.to_do_items
    assert len(items) == 2
    assert items[0].id == 'id_1'
    assert items[1].id == 'id_2'