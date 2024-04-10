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


# Connect to the server
sio.connect('http://walternicolas.de:80')

sio.emit('hello', "Data")
# Wait for the connection to establish
sio.wait()

