from main import socket, app

if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)