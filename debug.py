from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

FORMAT = 'utf-8'


def encryptMsg(msg, pubKey):
    pubKey = RSA.importKey(pubKey)

    # create a cipher object for the key
    cipher = PKCS1_OAEP.new(pubKey)
    
    #encrypt            (convert msg to bytes)
    output = cipher.encrypt(msg.encode())
    return output

def decryptMsg(msg, privKey):
    privKey = RSA.importKey(privKey)

    cipher = PKCS1_OAEP.new(privKey)

    output = cipher.decrypt(msg).decode(FORMAT)
    return output

# run
message = 'You can attack now!'

# get a key using random bytes
key = RSA.generate(2048, get_random_bytes)
# key means private key, pubKey means public key
# the public key is deriven from the private key, but not the other way around

# set keys from key
pubKey = key.publickey().export_key("OpenSSH")
privKey = key.export_key('PEM')

encryptedMsg = encryptMsg(message, pubKey)
decryptedMsg = decryptMsg(encryptedMsg, privKey)

print(f"Original:\n{message}\n\nEncrypted:\n{encryptedMsg}\n\nDecrypted:\n{decryptedMsg}")

""" 
#write Private Key to a pem file
with open('myKey.pem', 'wb') as f:
    f.write(key.export_key('PEM'))

#write the Public Key to a txt file
pubKey = key.publickey().export_key("OpenSSH")
with open('pubKey.pem', 'wb') as f:
    f.write(pubKey)

# ----this code could be run on a seperate script theoretically----

#get our public key (it's just gonna be a memory reference)
pubKey = RSA.importKey(open('pubKey.pem').read())
#okay now let's encrypt a message using pubKey

#create a cipher object for our key
cipher = PKCS1_OAEP.new(pubKey)

encryptedMsg = cipher.encrypt(message.encode())

print(f"\n    jumbled message:\n{encryptedMsg}\n\n")

#okay now decrypt
cipher = PKCS1_OAEP.new(key)

decryptedMsg = cipher.decrypt(encryptedMsg).decode('utf-8')

print(f"back to the original message:\n{decryptedMsg}")

print(f"is it the same? - {message == decryptedMsg}") """