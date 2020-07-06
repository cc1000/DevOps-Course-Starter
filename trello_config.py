root_url = 'https://api.trello.com/1'

def get_config(filename):
    file = open(f'trello_config/{filename}.txt')
    config = file.read()
    file.close()
    return config

api_key = get_config('api_key')
token = get_config('token')