root_url = 'https://api.trello.com/1'
board_id = '5ef8f1926a457142f41ac6ed'
todo_list_id = '5ef8f19a64a8ef61948d43fd'
done_list_id = '5ef8f19c4743080e63d5db1c'

def get_config(filename):
    file = open(f'trello_config/{filename}.txt')
    config = file.read()
    file.close()
    return config

api_key = get_config('api_key')
token = get_config('token')