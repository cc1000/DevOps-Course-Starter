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

def test_can_get_all_to_do_items(view_model):
    assert view_model.to_do_items == items