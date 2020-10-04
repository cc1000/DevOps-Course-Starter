from dotenv import find_dotenv, load_dotenv
from app import create_app

load_dotenv(find_dotenv('.env'))

application = create_app()

if __name__ == '__main__':
    application.run()