class ToDoItemsViewModel:
    def __init__(self, to_do_items):
        self._to_do_items = to_do_items

    @property
    def to_do_items(self):
        return self._to_do_items