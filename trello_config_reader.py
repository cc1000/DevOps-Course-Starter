def get_config(filename):
    file = open(f'trello_config/{filename}.txt')
    config = file.read()
    file.close()
    return config