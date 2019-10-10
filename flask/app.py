from flask import Flask, escape, request, redirect, send_from_directory, render_template
import pugsql

app = Flask(__name__)


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


@app.route('/home')
def home():
    page = {
        'title': "Home"
    }
    return render_template('home.html', page=page)


@app.route('/')
def root():
    return redirect("/home")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
