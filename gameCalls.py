from flask import request


def init(socketio):

    gamePins = []
    clients = []

    @socketio.on('connect')
    def connect():
        sid = request.sid
        clients.append(sid)
        print('Client connected', sid)

    @socketio.on('disconnect')
    def disconnect():
        sid = request.sid
        clients.remove(sid)
        print('Client disconnected')

    @socketio.on('newGamePin')
    def newGamePin():
        sid = request.sid
        pin = '123456'
        gamePins.append(sid)
        socketio.emit('gamePin', pin, room=sid)

    @socketio.on('hello')
    def hello(message):
        sid = request.sid
        print(message, sid)
        socketio.emit('hello', message, room=sid)

    @socketio.on('helloAll')
    def helloAll(message):
        sid = request.sid
        print(message, sid)
        socketio.emit('hello', message)

    @socketio.on('helloOthers')
    def helloOthers(message):
        sid = request.sid
        print(message, sid)
        socketio.emit('hello', message, include_self=False)
