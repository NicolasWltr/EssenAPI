from flask import request
import random


def init(socketio):
    gamePins = {}
    clientSid = {}
    clients = []

    nextClient = [1000]

    @socketio.on('connect')
    def connect():
        if len(clients) == 0:
            for i in range(0, 10):
                clients.append(str(i))
        clients.append(request.sid)
        print('Client connected')

    @socketio.on('disconnect')
    def disconnect():
        clients.pop(0)
        print('Client connected')

    @socketio.on('leaveGame')
    def leaveGame(gamePin, client):
        updateClient(client, request.sid)

        if gamePin in gamePins:
            del gamePins[gamePin][client]
        print(client, "left", gamePin)

    @socketio.on('getClient')
    def getClient():
        sid = request.sid
        socketio.emit('getClient', nextClient[0], room=sid)
        updateClient(nextClient[0], sid)
        nextClient[0] += 1

    @socketio.on('updateClient')
    def updateClient(client):
        updateClient(client, request.sid)

    @socketio.on('disconnectClient')
    def disconnect(client):
        clientSid.pop(client)
        removeUnusedSidFromGame()
        removeUnusedGamePin()
        print(gamePins)
        print('Client disconnected')

    @socketio.on('newGamePin')
    def newGamePin(client):
        updateClient(client, request.sid)
        pin = genPin()
        gamePins[pin] = []
        gamePins[pin].append(client)
        print(gamePins)
        socketio.emit('gamePin', pin, room=getSid(client))

    @socketio.on('connectToPin')
    def connectToPin(pin, client):
        updateClient(client, request.sid)
        removeUnusedGamePin()
        removeUnusedSidFromGame()
        if pin not in gamePins:
            print('Pin not found', pin)
            socketio.emit('ConnectedToGame', "Game Pin not found", room=getSid(client))
        if len(gamePins[pin]) >= 2:
            print('Game full', pin)
            socketio.emit('ConnectedToGame', "Game full", room=getSid(client))
            return

        print('Connecting to game pin', pin)
        gamePins[pin].append(client)
        mesAllMem(pin)

    @socketio.on('chatToGame')
    def chatToGame(mes, client):
        updateClient(client, request.sid)
        print("Chatting")

        mes = str(client) + "\n-> " + mes

        print(mes)

        gp = gpForSid(client)

        if gp == "":
            return

        for user in gamePins[gp]:
            print(user)
            socketio.emit('chat', mes, room=getSid(user))

    @socketio.on('GetGameState')
    def getGameState(client):
        updateClient(client, request.sid)

        print(client, "wants to get game state")

        gp = gpForSid(client)

        for user in gamePins[gp]:
            if user == client:
                break

            socketio.emit('GameStateReq', client, room=getSid(user))
            return

    @socketio.on('RespWithGameState')
    def RespWithGameState(state, clientToGet, client):
        updateClient(client, request.sid)
        print(client, "sends game state to", clientToGet)
        socketio.emit('GameStateResp', state, room=getSid(clientToGet))

    @socketio.on('UpdateCons')
    def UpdateCons(state, gPin, client):
        updateClient(client, request.sid)
        if gPin not in gamePins:
            print('Pin not found', gPin)

        for user in gamePins[gPin]:
            if user == client:
                pass
            print("update ", user)
            socketio.emit('getUpdatedFromPIN', state, room=getSid(user))

    def mesAllMem(pin):
        for user in gamePins[pin]:
            socketio.emit('ConnectedToGame', "Success", room=getSid(user))

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

    def removeUnusedSidFromGame():
        clientToRemove = {}
        for game in gamePins:
            for user in gamePins[game]:
                if user not in clientSid:
                    if not clientToRemove.__contains__(user):
                        clientToRemove[user] = []
                    clientToRemove[user].append(game)

        for user in clientToRemove:
            for game in clientToRemove[user]:
                gamePins[game].remove(user)

        clientToRemove.clear()

        for client in clientSid.values():
            print(client, "removemomveo")

    def gpForSid(client):
        gp = ""
        for game in gamePins:
            for user in gamePins[game]:
                if user == client:
                    gp = game

        return gp

    def updateClient(client, sid):
        if client in clientSid:
            clientSid.update({client: sid})
        else:
            clientSid[client] = sid

    def getSid(client):
        if client in clientSid:
            return clientSid[client]

        return "Undefined"
