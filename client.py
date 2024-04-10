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
sio.connect('http://192.168.178.68:6000')

# Wait for the connection to establish
sio.wait()
