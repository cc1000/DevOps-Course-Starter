from flask import Flask, render_template, request, redirect, url_for
import board_api as board_api
from to_do_items_view_model import ToDoItemsViewModel

app = Flask(__name__)

@app.route('/')
def index():
    to_do_items = sorted(board_api.get_items(), key=lambda item: item.status, reverse=True)
    view_model = ToDoItemsViewModel(to_do_items)
    return render_template('index.html', view_model=view_model)

@app.route('/', methods=['POST'])
def add():
    board_api.add_item(request.form['title'])
    return redirect(url_for('index'))

@app.route('/complete_item', methods=['GET'])
def complete_item():
    id = request.args.get('id')
    board_api.complete_item(id)
    return redirect(url_for('index'))

@app.route('/delete_item', methods=['GET'])
def delete_item():
    id = request.args.get('id')
    board_api.delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
