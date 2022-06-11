import rsa
from Crypto.PublicKey import RSA

# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be atleast 16
publicKey, privateKey = rsa.newkeys(512)

if False:
    #write to a file
    with open('pubKey.txt', 'w') as f:
        f.write(str(publicKey))
    #write to a file
    with open('privKey.txt', 'w') as f:
        f.write(str(privateKey))

#read a file
with open('pubKey.txt', 'r') as f:
    publicKey = RSA.importKey(f.read())

with open('privKey.txt', 'r') as f:
    privateKey = RSA.importKey(f.read())


# this is the string that we will be encrypting
message = "hello geeks".encode()

# rsa.encrypt method is used to encrypt
# string with public key string should be
# encode to byte string before encryption
# with encode method
print(f"\nmessage: {message}\n\n")
print(f"\npublicKey: {publicKey}\n\n")
print(f"\nprivateKey: {privateKey}\n\n")

encMessage = rsa.encrypt(message, publicKey)


"""
print(f"\nencrypted string: {encMessage}\n\n")

# the encrypted message can be decrypted
# with ras.decrypt method and private key
# decrypt method returns encoded byte string,
# use decode method to convert it to string
# public key cannot be used for decryption
print(f"\n\nprivKey: {privateKey}\n")
print(f"\n\nencMsg: {encMessage}\n")
decMessage = rsa.decrypt(encMessage, privateKey).decode()

print(f"\ndecrypted string: {decMessage}")
"""