import socket
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import rsa

from debug import decryptMsg

HEADER = 64
# get the port from a file for easier changing
with open('port.txt', 'r') as f:
    PORT = int(f.read())
FORMAT = 'ascii'
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
# the local information about who this client is ('[IPv4]', [addr])
localAddr = str(client)[95:119]

symKey = ''


def send(msg, myKey):
    # "why are you using myKey and key?"
    # because at first we don't want to encrypt some messages.
    # when global key gets set to msg recieve at the end of this func,
    # we start passing key as the second argument of this func from then on.
    # but we still need the ability to send non-encrypted messages to the server,
    # thus we have the double variable.
    # "Couldn't you just use a bool instead?"
    # probably, but I have more important things to work on here at the moment
    global symKey
    global secured
    message = msg.encode(FORMAT)
    #tell the client that we're switching keys, so we're not secure
    #until it gets set
    if message == KEY_REQUEST:      #[debug] this probably shouldn't exist, especially within send()
        secured = False
    #don't encrypt if we're sending an rsa key, or if we don't have a key to encrypt msg with
    if myKey == None:
        pass
    # if we're using fernet (symmetric)
    else:
        #encrypt using our key
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
    msgRecv = client.recv(2048)
    
    # if they don't have key (this is only the case if they're sending an rsa pubKey)
    if myKey == None:
        # decrypt the msgRecv from server using privKey, set the output as our symKey
        symKey = decryptMsg(msgRecv, privKey).encode()
        secured = True
        # make sure you only use fernet for encoding from here on out

    try:
        username = username
    except NameError:
        username = localAddr


    
    return msgRecv

secured = False

connected = True
while connected:
    if not secured:
        # generate a private RSA key
        rsaKeys = RSA.generate(2048, get_random_bytes)

        # set key variables
        pubKey = rsaKeys.publickey().export_key("OpenSSH")
        privKey = rsaKeys.export_key('PEM')

        # Send the key request tag, along with the public (asymmetric) key for the server 
        # to encrypt the symmetric key with. Pass None as the argument for key, since
        # we aren't encrypting.
        send(f"{KEY_REQUEST}::{pubKey.decode(FORMAT)}", None)

        secured = True
        # send a username
        username = input("Select a username:\n> ")

        # msg should look like: "!USERNAME::[some username]"
        send(f"{USERNAME_SET}::{username}", symKey)
    #once secured, start sending input() messages to server
    # get user input
    myMsg = input("Send Message:\n> ")
    #if they say 'quit' or 'q', disconnect them
    if myMsg in ("quit", "q"):
        connected = False
        myMsg = DISCONNECT_MESSAGE
    # otherwise, send the message
    send(myMsg, symKey)

print("you have been disconnected.")