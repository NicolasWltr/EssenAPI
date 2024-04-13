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

    @socketio.on('connectToPin')
    def connectToPin(pin):
        sid = request.sid
        if pin not in gamePins:
            print('Pin not found', pin)
            socketio.emit('connectToGamePin', "No game pins found", room=sid)
        if len(gamePins[pin]) >= 2:
            print('Game full', pin)
            socketio.emit('connectToGamePin', "No game pins found", room=sid)
            return

        print('Connecting to game pin', pin)
        gamePins[pin].append(sid)
        mesAllMem(pin)

    @socketio.on('chatToGame')
    def chatToGame(mes):
        sid = request.sid
        gp = ""
        for game in gamePins:
            for user in gamePins[game]:
                if user == sid:
                    gp = game
        for user in gamePins[gp]:
            socketio.emit('chat', mes, room=user)

    def mesAllMem(pin):
        for user in gamePins[pin]:
            socketio.emit('AllConnected', room=user)

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
