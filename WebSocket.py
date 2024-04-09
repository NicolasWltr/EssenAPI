from main import socket


@socket.on('connect')
def connect():
    print("Client")


@socket.on('checker')
def checker(data):
    socket.send(data)