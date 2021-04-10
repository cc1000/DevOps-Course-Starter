from datetime import date
from to_do_item import ToDoItem
from auth_provider import AuthProvider

class ToDoItemsViewModel:
    def __init__(self, user, items):
        self.user_is_writer = self.user_is_writer(user)
        self._items = items

    def user_is_writer(self, user):
        return AuthProvider.WRITER_ROLE in user.roles

    @property
    def all_items(self):
        return self._items

    @property
    def to_do_items(self):
        return [item for item in self.all_items if item.status == ToDoItem.to_do_status]

    @property
    def completed_items(self):
        return [item for item in self.all_items if item.status == ToDoItem.completed_status]

    @property
    def show_all_completed_items(self):
        return len(self.completed_items) < 5

    @property
    def recent_completed_items(self):
        return None if self.show_all_completed_items else [item for item in self.completed_items if item.last_modified.date() == date.today()]

    @property
    def older_completed_items(self):
        return None if self.show_all_completed_items else [item for item in self.completed_items if item.last_modified.date() < date.today()]