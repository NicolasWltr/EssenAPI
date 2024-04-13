from flask import request
import random


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
        pin = genPin()
        print(pin)
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

    def genPin():
        pin = random.randint(100000, 999999)
        while pin in gamePins:
            pin = random.randint(100000, 99999999)

        return pin
