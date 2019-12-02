from flask import Flask, request, redirect, send_from_directory, render_template, g, session
import pugsql
from flask_socketio import SocketIO
import string
import random
import datetime as dt
import sys

app = Flask(__name__)
# crypt key fot the session
app.secret_key = 'tatsuatshisadlmaòcisoia69420'
socketio = SocketIO(app)

# Root handler
@app.route('/')
def root():
    return redirect("/home")


def refresh_the_client():
    # Sends a message via WebSocket to the browser
    # to refresh the page
    socketio.emit("refresh", "Refresh")

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page not found")

# send the js files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

# send the css files
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

# send the image files
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)


# take the string after /add_user/ and append it as username in the session
@app.route('/add_user/<string:name>')
def add_user(name):

    data = {
        'userName': ''.join(random.choices(string.ascii_lowercase, k=5)),
        'userSurname': ''.join(random.choices(string.ascii_lowercase, k=5)),
        'userID': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'userRole': random.choice(['Studente', 'Professore'])
    }

    if 'users' in session:
        if data not in session['users']:
            session['users'].append(data)
            session.modified = True

    refresh_the_client()
    return redirect('/home')


@app.route('/post_user', methods=['POST'])
def post_user():
    if request.method == 'POST':
        data = request.get_json()
        print(data, file=sys.stdout)
        if 'users' in session:
            if data not in session['users'] or True:
                session['users'].append(data)
                session.modified = True
        refresh_the_client()
        return redirect('/home')

    if request.method == 'GET':
        pass


@app.route('/button2')
def button1():
    socketio.emit("next", "next")
    return redirect("/home")


# clear the session
@app.route('/clear')
def clear():
    session.clear()
    refresh_the_client()
    return redirect('/home')

# home root handler
@app.route('/home')
def home():
    if not 'users' in session:
        session['users'] = []

    print(session['users'])

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
            "href": "/add_user/a"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "/date"
        }]
    }

    return render_template('home.html', page=page)

# date root handler
@app.route('/date')
def date():
    if not 'users' in session:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    days = [(dt.datetime.now() + dt.timedelta(days=i)).date()
            for i in range(0, 7)]
    print(days)

    page = {
        'title': "Pronatozione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "/clear"
        }, {
            "name": "Cambia giorno",
            "color": "green",
            "href": "/button1"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }],
        'days': days
    }

    return render_template('date.html', page=page)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
