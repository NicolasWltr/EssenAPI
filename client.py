import socketio

# Create a SocketIO client instance
sio = socketio.Client()


# Define event handlers
@sio.event
def connect():
    print('Connected to server')


@sio.event
def disconnect():
    print('Disconnected from server')


@sio.event
def hello(message):
    print(message)


# Connect to the server
sio.connect('ws://walternicolas.de:80')
print('con')
print('fin')
sio.emit('hello', "Data")
# Wait for the connection to establish

sio.wait()
