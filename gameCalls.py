from flask import request
import random


def init(socketio):

    gamePins = {}
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
        removeUnusedGamePin()
        print(gamePins)
        print('Client disconnected')

    @socketio.on('newGamePin')
    def newGamePin():
        sid = request.sid
        pin = genPin()
        gamePins[pin] = []
        gamePins[pin].append(sid)
        print(gamePins)
        socketio.emit('gamePin', pin, room=sid)

    def genPin():
        pin = random.randint(100000, 999999)
        while pin in gamePins:
            pin = random.randint(100000, 99999999)

        return pin

    def removeUnusedGamePin():
        pinsToRem = []
        for pin in gamePins:
            for user in gamePins[pin]:
                if user not in clients:
                    pinsToRem.append(pin)

        for pin in pinsToRem:
            del gamePins[pin]
