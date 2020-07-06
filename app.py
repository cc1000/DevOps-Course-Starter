from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)

@app.route('/')
def index():
    items = session.get_items()
    toDoItems = sorted(session.get_items(), key=lambda item: item.status, reverse=True)
    return render_template('index.html', toDoItems=toDoItems)

@app.route('/', methods=['POST'])
def add():
    session.add_item(request.form['title'])
    return redirect(url_for('index'))

@app.route('/complete_item', methods=['GET'])
def complete_item():
    id = request.args.get('id')
    session.complete_item(id)
    return redirect(url_for('index'))

@app.route('/delete_item', methods=['GET'])
def delete_item():
    id = request.args.get('id')
    session.delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
