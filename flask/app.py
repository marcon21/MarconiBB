from flask import Flask, request, redirect, send_from_directory, render_template, g  # , session
import pugsql
from flask_socketio import SocketIO
import string
import random
import datetime as dt
import sys
import json

app = Flask(__name__)
# crypt key fot the session
# app.secret_key = 'tatsuatshisadlmaòcisoia69420'
app.secret_key = "".join(random.choices(string.ascii_lowercase, k=15))
socketio = SocketIO(app)

session = {}
current_page = None

month = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
         'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

dayTranslation = {
    'Mon': 'Lunedì',
    'Tue': 'Martedì',
    'Wed': 'Mercoledì',
    'Thu': 'Giovedì',
    'Fri': 'Venerdì',
    'Sat': 'Sabato',
    'Sun': 'Domenica'
}

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

    refresh_the_client()
    return redirect('/home')


@app.route('/post_user', methods=['POST'])
def post_user():
    if request.method == 'POST':
        data = json.loads(request.get_json(cache=False))

        if 'users' in session.keys():
            if data not in session['users']:
                session['users'].append(data)

        refresh_the_client()

        return "Nais"


@app.route('/button1')
def button1():
    return redirect('/clear')


@app.route('/button2')
def button2():
    if current_page == 'home':
        pass
    elif current_page == 'date' or current_page == 'hour':
        socketio.emit("next", "next")
    return "Ok"


@app.route('/button3')
def button3():
    socketio.emit("changePage", "changePage")
    return "Ok"


# clear the session
@app.route('/clear')
def clear():
    session.clear()
    refresh_the_client()
    return "Ok"

# home root handler
@app.route('/home')
def home():
    current_page = 'home'

    if not 'users' in session:
        session['users'] = []

    page = {
        'title': "Prenotozione Aula",
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
    current_page = 'date'

    if not 'users' in session:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    n_days = 7
    week = [None for _ in range(0, n_days)]

    for i in range(0, n_days):
        day = (dt.datetime.now() + dt.timedelta(days=i)).date()
        week[i] = {
            'day': day.day,
            'daySpelled': dayTranslation[day.strftime("%a")],
            'month': month[day.month - 1]
        }

    days = []
    for day in week:
        if day['daySpelled'] != "Domenica":
            days.append(day)

    page = {
        'title': "Prenotazione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "/clear"
        }, {
            "name": "Cambia giorno",
            "color": "green",
            "href": ""
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
