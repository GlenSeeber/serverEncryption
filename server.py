import socket 
import threading
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HEADER = 64
PORT = 5060
# my linux laptop: 192.168.1.45
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
KEY_REQUEST = '!SEND_KEY'
KEY_CONFIRMED = '!KEY_CONFIRMED'
DISCONNECT_MESSAGE = "!DISCONNECT"
USERNAME_SET = "!USERNAME"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

userAddrBook = {}

def convert(string, breaker):
    li = list(string.split(breaker))
    return li

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
            # decode if necessary
            if secured:
                msg = fernet.decrypt(msg)
            msg = msg.decode(FORMAT)
            # pull username from our address book dictionary
            try:
                username = userAddrBook[str(addr)]
            except KeyError:
                username = str(addr)
            print(f"[Message Recieved ({username})] {msg}")
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
            elif USERNAME_SET in msg:
                # incoming message should look like:
                # "!USERNAME::[some username]"

                # seperate the actual content from the starting tag
                userAddr = convert(msg, '::')[1]
                print(f"userAddr: {userAddr} (ln 80)")     #debug

                # should look like: 
                # {"[some username]":"[some address]"}
                userAddrBook.update({userAddr[0] : str(addr)})
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