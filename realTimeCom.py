from flask import request
import random


def init(socketio):
    @socketio.on('RTCom')
    def handle_RTCom(client):
        socketio.emit('RTCom', random.randint(0, 1000), room=request.sid)

