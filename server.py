import socket 
import threading
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HEADER = 64
PORT = 5000
# my linux laptop: 192.168.1.45
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
KEY_REQUEST = '!SEND_KEY'
KEY_CONFIRMED = '!KEY_CONFIRMED'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    #have we set up encryption yet
    secured = False
    
    connected = True
    while connected:
        output = 'DEFAULT_OUTPUT_MESSAGE'

        #check for a header being sent every loop
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # if we recieve a transmission
        if msg_length:
            #so that the server doesn't crash, it will just cleanly disconnect you
            try:
                msg_length = int(msg_length)
            except:
                datatypeError = "incorrect data type sent, disconnecting from client"
                print(datatypeError)
                conn.send(datatypeError)
                break
            # recieve the message
            msg = conn.recv(msg_length)
            tags = ''
            # decode if necessary
            if secured:
                msg = fernet.decrypt(msg)
                tags += 'DECRYPTED, '
            msg = msg.decode(FORMAT)
            print(f"[Message Recieved ({tags})] {msg}")
            # disconnect
            if msg == DISCONNECT_MESSAGE:
                connected = False
            # request key
            elif msg == KEY_REQUEST:
                key = Fernet.generate_key()
                fernet = Fernet(key)
                print(f"key generated:\n{key}\n")
                output = key
                # we will now be communicating exclusively through encrypted messages
                secured = True
            #send the output
            try:
                output = output.encode(FORMAT)
            except:
                pass
            conn.send(output)

        if not secured:
            conn.send(key)

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()