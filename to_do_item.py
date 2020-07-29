class ToDoItem:
    to_do_status = 'To Do'
    completed_status = 'Completed'

    def __init__(self, id, name, status):
        self.id = id
        self.title = name
        self.status = status

    @staticmethod
    def from_trello_data(trello_item_data, done_list_id):
        return ToDoItem(
            trello_item_data['id'], 
            trello_item_data['name'],
            'Completed' if trello_item_data['idList'] == done_list_id else 'To Do'
        )