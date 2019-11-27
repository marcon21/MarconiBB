from flask import Flask, request, redirect, send_from_directory, render_template, g, session
import pugsql
from flask_socketio import SocketIO, emit
import string
import random

app = Flask(__name__)
# crypt key fot the session
app.secret_key = 'tatsuatshisadlmaòcisoia69420'
socketio = SocketIO(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page not found")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)


# take the string after /add_user/ and append it as username in the session
@app.route('/add_user/<string:name>')
def add_user(name):
    if 'users' in session:
        if {'name': name} not in session['users']:
            session['users'].append({'name': name})
            session.modified = True

    refresh_the_client()
    return redirect('/home')


# clear the session
@app.route('/clear')
def clear():
    session.clear()
    refresh_the_client()
    return redirect('/home')


@app.route('/home')
def home():
    if not 'users' in session:
        session['users'] = []

    new_user = ''.join(random.choices(string.ascii_lowercase, k=10))

    page = {
        'title': "Pronatozione Aula",
        'users': session['users'],
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "/clear"
        }, {
            "name": "Aggiungi Utente",
            "color": "green",
            "href": "http://localhost:5000/add_user/{}".format(new_user)
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }]
    }

    return render_template('home.html', page=page)


@app.route('/')
def root():
    return redirect("/home")


def refresh_the_client():
    socketio.send("Refresh")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
