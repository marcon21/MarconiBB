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
test_mode = True

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


def getRoom():
    # if False not in [el in session for el in ["a", "b"]]:

    if all(el in session.keys() for el in ['users', 'selectedDay', 'startingHour', 'endingHour', 'type']):
        if test_mode:
            return session['type'] + str(random.randint(1, 4)) + str(random.randint(1, 30))
        else:
            # Future marconiTT Connection
            pass

    return "Error"


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
            if test_mode:
                session['users'] = [
                    {
                        'userName': 'Daniel',
                        'userSurname': 'Marcon',
                        'userID': '1',
                        'userRole': 'Studente'
                    }, {
                        'userName': 'Giacomo',
                        'userSurname': 'Tezza',
                        'userID': '1',
                        'userRole': 'Studente'
                    }, {
                        'userName': 'Enea',
                        'userSurname': 'Strambini',
                        'userID': '1',
                        'userRole': 'Studente'
                    }
                ]
            else:
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
    print(current_page, file=sys.stderr)
    if current_page == 'home':
        add = add_user(" ")
    elif current_page == 'date' or current_page == 'hour' or current_page == 'type':
        socketio.emit("next", "next")
    return redirect("/buttons")


@app.route('/button3')
def button3():
    socketio.emit("changePage", "changePage")
    return redirect("/buttons")


@socketio.on("daySelected")
def daySelected(message):
    global session
    days = get_days()
    session['selectedDay'] = days[message['dayIndex']]


@socketio.on("hourSelected")
def hourSelected(message):
    global session
    session['startingHour'] = message['startingHour']
    session['endingHour'] = message['endingHour']


@socketio.on("typeSelected")
def typeSelected(message):
    global session
    session['type'] = message['type']
    print(session, file=sys.stderr)


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
    hours = [{'name': '{} Ora'.format(i), 'startTime': str(i+7)+":00", 'endTime': str(i+7)+":55"}
             for i in range(1, 11)]
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
            "href": "",
            "id": "button1"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "",
            "id": "button3"
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
            "href": "/button1",
            "id": "button1"
        }, {
            "name": "Button2",
            "color": "amber darken-1",
            "href": "/button2",
            "id": "button2"
        }, {
            "name": "Button3",
            "color": "blue",
            "href": "/button3",
            "id": "button3"
        }]
    }

    return render_template('buttons.html', page=page)


# date page handler
@app.route('/date')
def date():
    global current_page

    if not 'users' in session or len(session['users']) < 1:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    current_page = 'date'

    days = get_days()

    page = {
        'title': "Prenotazione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "",
            "id": "button1"
        }, {
            "name": "Cambia giorno",
            "color": "amber darken-1",
            "href": "",
            "id": "button2"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "",
            "id": "button3"
        }],
        'days': days
    }

    return render_template('date.html', page=page)


# hour page handler
@app.route('/hour')
def hour():
    global current_page

    if not 'users' in session or len(session['users']) < 1:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    current_page = 'hour'

    hours = get_hours()
    # print(hours, file=sys.stderr)
    page = {
        'title': "Prenotazione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "",
            "id": "button1"
        }, {
            "name": "Cambia ora",
            "color": "amber darken-1",
            "href": "",
            "id": "button2"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "",
            "id": "button3"
        }],
        'hours': hours
    }

    return render_template('hour.html', page=page)


# type page handler
@app.route('/type')
def type():
    global current_page

    if not 'users' in session or len(session['users']) < 1:
        return redirect("/home")
    if len(session['users']) < 1:
        return redirect("/home")

    current_page = 'type'

    types = [{
        'name': "Aula"
    }, {
        'name': "Laboratorio"
    }]

    page = {
        'title': "Prenotazione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "",
            "id": "button1"
        }, {
            "name": "Cambia tipo",
            "color": "amber darken-1",
            "href": "",
            "id": "button2"
        }, {
            "name": "Avanti",
            "color": "blue",
            "href": "",
            "id": "button3"
        }],
        'types': types
    }

    return render_template('type.html', page=page)  # type page handler


@app.route('/confirmation')
def confirmation():
    global current_page

    room = getRoom()
    if room == "Error":
        return redirect('/home')

    current_page = 'confirmation'

    page = {
        'title': "Prenotazione Aula",
        'buttons': [{
            "name": "Annulla",
            "color": "red",
            "href": "",
            "id": "button1"
        }, {
            "name": "Conferma",
            "color": "blue",
            "href": "",
            "id": "button3"
        }],
        'roomInfo': {
            'users': session['users'],
            'day': session['selectedDay'],
            'startingHour': session['startingHour'],
            'endingHour': session['endingHour'],
            'room': room
        }
    }

    return render_template('confirmation.html', page=page)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
