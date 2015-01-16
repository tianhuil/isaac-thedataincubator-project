from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def javascript(path):
    return app.send_static_file(os.path.join('js', path))

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(os.path.join('static', path))

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
