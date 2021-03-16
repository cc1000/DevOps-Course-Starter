from flask import Flask, render_template, request, redirect, url_for
import board_repository as board_repository
from to_do_items_view_model import ToDoItemsViewModel

def create_app():
    app = Flask(__name__)

    @app.route('/')
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
