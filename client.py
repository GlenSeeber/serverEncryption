import socket
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import rsa

HEADER = 64
# get the port from a file for easier changing
with open('port.txt', 'r') as f:
    PORT = int(f.read())
FORMAT = 'utf-8'
KEY_REQUEST = '!SEND_KEY'
KEY_CONFIRMED = '!KEY_CONFIRMED'
DISCONNECT_MESSAGE = "!DISCONNECT"
USERNAME_SET = "!USERNAME"

# what is the IP address to the server you are connecting to?
# if you're running this locally, you'll need the private IP
# pull the ip from a file for an easy way to update it
with open('serverIP.txt', 'r') as f:
    SERVER = f.read()
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

key = ''


def send(msg, myKey, type='rsa'):
    # "why are you using myKey and key?"
    # because at first we don't want to encrypt some messages.
    # when global key gets set to msg recieve at the end of this func,
    # we start passing key as the second argument of this func from then on.
    # but we still need the ability to send non-encrypted messages to the server,
    # thus we have the double variable.
    # "Couldn't you just use a bool instead?"
    # probably, but I have more important things to work on here at the moment
    global key
    global secured
    message = msg.encode(FORMAT)
    #tell the client that we're switching keys, so we're not secure
    #until it gets set
    if message == KEY_REQUEST:
        secured = False
    #if we're using rsa (asymmetric)
    if type == 'rsa':
        #don't encrypt the message, we're sending a public Key
        pass
    # if we're using fernet (symmetric)
    elif type == 'fernet':
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
    
    if type == 'rsa':
        key = rsa.decrypt(msgRecv, privKey)
        secured = True
        type = 'fernet'

    print(f"[SERVER] {msgRecv}")
    return msgRecv

secured = False

connected = True
while connected:
    if not secured:
        pubKey, privKey = rsa.newkeys(512)
        #send the key request tag, along with the public (asymmetric) key for the server 
        # to encrypt the symmetric key with, and send over to us.
        send(f"{KEY_REQUEST}::{pubKey}", privKey)
        print(f"public key:\n{pubKey}")

        secured = True
        # send a username
        username = input("Select a username:\n> ")

        # msg should look like: "!USERNAME::[some username]"
        send(f"{USERNAME_SET}::{username}", key)
    #once secured, start sending input() messages to server
    # get user input
    myMsg = input("Send Message:\n> ")
    #if they say 'quit' or 'q', disconnect them
    if myMsg in ("quit", "q"):
        connected = False
        myMsg = DISCONNECT_MESSAGE
    # otherwise, send the message
    send(myMsg, key)

print("you have been disconnected.")