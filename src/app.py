from flask import Flask, render_template, request, redirect, url_for
from board_repository import BoardRepository
from to_do_items_view_model import ToDoItemsViewModel
from flask_login import LoginManager, login_required, login_user
from app_user import AppUser
from auth_provider import AuthProvider
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "some_key"
    app.config['LOGIN_DISABLED'] = os.environ['AUTHENTICATION_DISABLED'] == 'True'

    board_repository = BoardRepository()
    auth_provider = AuthProvider()
    login_manager = LoginManager()

    @app.route('/')
    @login_required
    def index():
        to_do_items = sorted(board_repository.get_items(), key=lambda item: item.status, reverse=True)
        view_model = ToDoItemsViewModel(to_do_items)
        return render_template('index.html', view_model=view_model)

    @app.route('/', methods=['POST'])
    @login_required
    def add():
        board_repository.add_item(request.form['title'])
        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['GET'])
    @login_required
    def complete_item():
        board_repository.complete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @app.route('/delete_item', methods=['GET'])
    @login_required
    def delete_item():
        board_repository.delete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(auth_provider.get_login_redirect_uri())

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        user = auth_provider.get_authenticated_user(request.args.get('code'))
        login_user(user)

        return redirect(url_for('index'))

    @login_manager.user_loader
    def load_user(user_id):
        return auth_provider.get_user(user_id)

    login_manager.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()