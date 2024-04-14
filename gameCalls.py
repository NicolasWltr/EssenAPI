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
        removeUnusedGamePin()
        removeUnusedSidFromGame()
        sid = request.sid
        if pin not in gamePins:
            print('Pin not found', pin)
            socketio.emit('ConnectedToGame', "Game Pin not found", room=sid)
        if len(gamePins[pin]) >= 2:
            print('Game full', pin)
            socketio.emit('ConnectedToGame', "Game full", room=sid)
            return

        print('Connecting to game pin', pin)
        gamePins[pin].append(sid)
        mesAllMem(pin)

    @socketio.on('chatToGame')
    def chatToGame(mes):
        sid = request.sid

        mes = sid + "\n-> " + mes

        gp = gpForSid(sid)

        if gp == "":
            return

        for user in gamePins[gp]:
            socketio.emit('chat', mes, room=user)

    @socketio.on('GetGameState')
    def getGameState():
        sid = request.sid

        gp = gpForSid(sid)

        for user in gamePins[gp]:
            if user == sid:
                return

            socketio.emit('GameStateReq', sid, room=user)

    @socketio.on('RespWithGameState')
    def RespWithGameState(state, sid):
        print(sid)
        print(state)
        socketio.emit('GameStateResp', state, room=sid)

    @socketio.on('UpdateCons')
    def UpdateCons(state, gPin):
        if not gamePins.get(gPin):
            print("Game pin not found", gPin)

        for user in gamePins[gPin]:
            print("update ", user)
            socketio.emit('getUpdatedFromPIN', state, room=user)

    def mesAllMem(pin):
        for user in gamePins[pin]:
            socketio.emit('ConnectedToGame', "Success", room=user)

    def genPin():
        pin = random.randint(100000, 999999)
        while pin in gamePins:
            pin = random.randint(100000, 99999999)

        return pin

    def removeUnusedGamePin():
        pinsToRem = []
        for pin in gamePins:
            if len(gamePins[pin]) == 0:
                pinsToRem.append(pin)

        for pin in pinsToRem:
            del gamePins[pin]

        removeUnusedSidFromGame()

    def removeUnusedSidFromGame():
        sidToRemove = {}
        for game in gamePins:
            for user in gamePins[game]:
                if user not in clients:
                    if not sidToRemove.__contains__(user):
                        sidToRemove[user] = []
                    sidToRemove[user].append(game)

        for user in sidToRemove:
            for game in sidToRemove[user]:
                gamePins[game].remove(user)

    def gpForSid(sid):
        gp = ""
        for game in gamePins:
            for user in gamePins[game]:
                if user == sid:
                    gp = game

        return gp
