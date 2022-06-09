import socket
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HEADER = 64
PORT = 5000
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

key = ''


def send(msg, myKey=''):
    global key
    global secured
    message = msg.encode(FORMAT)
    #tell the client that we're switching keys, so we're not secure
    #until it gets set
    if message == KEY_REQUEST:
        secured = False
    #encrypt message if they passed an arg for key
    if myKey != '':
        fernet = Fernet(myKey)
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
    #reset the key if we request a new one
    if not secured:
        key = msgRecv
        secured = True
    return msgRecv

secured = False

connected = True
while connected:
    if not secured:
        send(KEY_REQUEST)
        print(f"key:\n{key}")
        secured = True
    #once secured, start sending input() messages to server
    # get user input
    myMsg = input("Send Message:\n> ")
    #if they say 'quit' or 'q', disconnect them
    if myMsg in ("quit", "q"):
        connected = False
        myMsg = DISCONNECT_MESSAGE
    # otherwise, send the message
    send(myMsg, key)

input("you have been disconnected.")