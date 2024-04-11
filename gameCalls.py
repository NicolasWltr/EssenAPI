from flask import request


def init(socketio):
    @socketio.on('connect')
    def connect():
        sid = request.sid
        print('Client connected', sid)

    @socketio.on('disconnect')
    def disconnect():
        print('Client disconnected')

    @socketio.on('hello')
    def hello(message):
        sid = request.sid
        print(message, sid)
        socketio.emit('hello', message, room=sid)

    @socketio.on('helloAl')
    def helloAll(message):
        sid = request.sid
        print(message, sid)
        socketio.emit('hello', message)
