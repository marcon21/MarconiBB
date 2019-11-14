from flask import Flask, request, redirect, send_from_directory, render_template, g, session
import pugsql

app = Flask(__name__)

# crypt key fot the session
app.secret_key = 'hdsadòsadhcisoia69420'


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
        session['users'].append({'name':name})
        session.modified = True
    return redirect('/home')


@app.route('/home')
def home():
    #session.clear()
    if not 'users' in session:
        session['users'] = []

    page = {
        'title': "Pronatozione Aula",
        'users': session['users']
    }
    return render_template('home.html', page=page)


@app.route('/')
def root():
    return redirect("/home")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
