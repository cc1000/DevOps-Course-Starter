from to_do_item import ToDoItem

class ToDoItemsViewModel:
    def __init__(self, to_do_items):
        self._to_do_items = to_do_items

    @property
    def all_items(self):
        return self._to_do_items

    @property
    def to_do_items(self):
        return [item for item in self.all_items if item.status == ToDoItem.to_do_status]

    @property
    def completed_items(self):
        return [item for item in self.all_items if item.status == ToDoItem.completed_status]