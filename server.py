import socket
from threading import Thread

from pynput.keyboard import Controller, Key
from screeninfo import get_monitors

SERVER = None
PORT = 8080
IP_ADDRESS = "192.168.0.100"
screen_width = None
screen_height = None

keyboard = Controller()


def acceptConnections():
    global SERVER
    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")
        thread1 = Thread(target=recvMsg, args=(client_socket,))
        thread1.start()


def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split("width=")[1])
        screen_height = int(str(m).split(",")[3].strip().split("height=")[1])


def recvMsg(client_socket):
    global keyboard
    while True:
        try:
            message = client_socket.recv(4096).decode()
            print(message)
            if message:
                keyboard.press(message)
                keyboard.release(message)
                print(message)
        except Exception:
            pass


def setup():
    print("Welcome To Remote Mouse")
    global SERVER
    global PORT
    global IP_ADDRESS
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print("Server listening...")
    getDeviceSize()
    acceptConnections()


setup()
