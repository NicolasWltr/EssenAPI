from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '12309812093'

socketio = SocketIO(app)


@app.route('/')
def index():
    return "MainTemp"


@socketio.on('connect')
def connect():
    print('Client')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)