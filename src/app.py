from flask import Flask, render_template, request, redirect, url_for
from board_repository import BoardRepository
from to_do_items_view_model import ToDoItemsViewModel
from flask_login import LoginManager, login_required

def create_app():
    app = Flask(__name__)
    board_repository = BoardRepository()
    login_manager = LoginManager()

    @app.route('/')
    @login_required
    def index():
        to_do_items = sorted(board_repository.get_items(), key=lambda item: item.status, reverse=True)
        view_model = ToDoItemsViewModel(to_do_items)
        return render_template('index.html', view_model=view_model)

    @app.route('/', methods=['POST'])
    def add():
        board_repository.add_item(request.form['title'])
        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['GET'])
    def complete_item():
        board_repository.complete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @app.route('/delete_item', methods=['GET'])
    def delete_item():
        board_repository.delete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @login_manager.user_loader
    def load_user(user_id):
        return None

    @login_manager.unauthorized_handler
    def unauthenticated():
        pass # TODO: Redirect to GitHub

    login_manager.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
