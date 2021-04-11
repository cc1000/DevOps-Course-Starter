class ToDoItem:
    to_do_status = 'To Do'
    completed_status = 'Completed'

    def __init__(self, id, name, status, last_modified):
        self.id = id
        self.title = name
        self.status = status
        self.last_modified = last_modified