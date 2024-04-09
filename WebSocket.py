from main import socket


@socket.on('connect')
def connect():
    print("Connected")


@socket.on('checker')
def checker(message):
    socket.send("Test")


