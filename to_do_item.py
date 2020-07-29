class ToDoItem:
    def __init__(self, trello_item_data, done_list_id):
        self.id = trello_item_data['id']
        self.title = trello_item_data['name']
        self.status = 'Completed' if trello_item_data['idList'] == done_list_id else 'To Do'