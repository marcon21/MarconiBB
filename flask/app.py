from flask import Flask, request, redirect, send_from_directory, render_template, g
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
    global current_page
    current_page = 'home'
    session.clear()
    refresh_the_client()
    return redirect("/buttons")


@app.route('/button2')
def button2():
    # print(current_page, file=sys.stderr)
    if current_page == 'home':
        pass
    elif current_page == 'date' or current_page == 'hour':
        socketio.emit("next", "next")
    return redirect("/buttons")


@app.route('/button3')
def button3():
    socketio.emit("changePage", "changePage")
    return redirect("/buttons")


@socketio.on("daySelected")
def daySelected(message):
    global session
    i = message['dayIndex']
    days = get_days()
    session['daySelected'] = days[i]
    print(session['daySelected'], file=sys.stderr)


@socketio.on("typeSelected")
def typeSelected(message):
    global session
    pass


@socketio.on("hourSelected")
def hourSelected(message):
    global session
    pass

# clear the session
@app.route('/clear')
def clear():
    global current_page
    current_page = 'home'
    session.clear()
    refresh_the_client()
    return "Ok"


def get_days():
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

    return days


def get_hours():
    hours = [{'name': '{} Ora'.format(i), 'startTime': str(
        random.randint(0, 12))} for i in range(10)]
    return hours

# home root handler
@app.route('/home')
def home():
    global current_page
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


# buttons page handler (for debug purposes)
@app.route('/buttons')
def buttons():
    if not 'users' in session:
        session['users'] = []

    page = {
        'title': "Prenotozione Aula",
        'users': session['users'],
        'buttons': [{
            "name": "Button1",
            "color": "red",
            "href": "/button1"
        }, {
            "name": "Button2",
            "color": "green",
            "href": "/button2"
        }, {
            "name": "Button3",
            "color": "blue",
            "href": "/button3"
        }]
    }

    return render_template('buttons.html', page=page)


# date page handler
@app.route('/date')
def date():
    global current_page
    current_page = 'date'

    if not 'users' in session:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    days = get_days()

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


# hour page handler
@app.route('/hour')
def hour():
    global current_page
    current_page = 'hour'

    if not 'users' in session:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    hours = get_hours()
    print(hours, file=sys.stderr)
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
        'startingHour': hours,
        'endingHour': hours

    }

    return render_template('hour.html', page=page)


# type page handler
@app.route('/type')
def type():
    global current_page
    current_page = 'type'

    if not 'users' in session:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    days = get_days()

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
