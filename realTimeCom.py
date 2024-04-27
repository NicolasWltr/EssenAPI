from flask import request


def init(socketio):
    @socketio.on('RTCom')
    def handle_RTCom(client):
        socketio.emit('RTCom', room=request.sid)

