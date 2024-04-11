from main import socketio


print('Hi')


@socketio.on('connect')
def connect():
    print('Client connected')


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


@socketio.on('hello')
def hello(message):
    print(message)
    socketio.emit('hello', message)
