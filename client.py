import socket
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
KEY_REQUEST = '!SEND_KEY'
KEY_CONFIRMED = '!KEY_CONFIRMED'
DISCONNECT_MESSAGE = "!DISCONNECT"
# what is the IP address to the server you are connecting to?
# if you're running this locally, you'll need the private IP
SERVER = "192.168.1.45"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg, key=''):
    message = msg.encode(FORMAT)
    #encrypt message if they passed an arg for key
    if key != '':
        fernet = Fernet(key)
        message = fernet.encrypt(message)
    # create header
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    #send to server
    client.send(send_length)
    client.send(message)
    # recieve a message back from the server
    msgRecv = client.recv(2048).decode(FORMAT)
    return msgRecv

secured = False

connected = True
while connected:
    if not secured:
        key = send(KEY_REQUEST)
        print(f"key:\n{key}")
        secured = True
    #once secured, start sending input() messages to server
    else:
        # get user input
        myMsg = input("Send Message:\n> ")
        #if they say 'quit' or 'q', disconnect them
        if myMsg in ("quit", "q"):
            break
        # otherwise, send the message
        send(myMsg, key)

#when they exit the loop, discconect them
send(DISCONNECT_MESSAGE)