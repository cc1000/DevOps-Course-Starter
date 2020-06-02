from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    toDoItems = sorted(session.get_items(), key=lambda item: item['status'], reverse=True)
    return render_template('index.html', toDoItems=toDoItems)

@app.route('/', methods=['POST'])
def add():
    session.add_item(request.form['title'])
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete():
    id = int(request.form['id'])
    toDoItem = session.get_item(id)
    toDoItem['status'] = 'Completed'
    session.save_item(toDoItem)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove():
    session.remove_item(int(request.form['id']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
