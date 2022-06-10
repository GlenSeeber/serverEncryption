import rsa
from cryptography.fernet import Fernet

def convert(string, breaker):
    li = list(string.split(breaker))
    return li

# msg contains the public key
msg = "!SEND_KEY::PublicKey(8048476234717738932734989159515624270210214717354379368403794219887970986450405471004819145347376598718294789720508485696447068834108248875002388186192013, 65537)"

#isolate
pubKey = convert(msg, '::')[1]
# encode into bytes
pubKey = pubKey.encode()

#print(f"public key recieved:\n{pubKey}\n")
"""
key = Fernet.generate_key()
fernet = Fernet(key)
"""

key = 'hello geeks'.encode()

# encrypt the symmetric key using the public asymmetric key that
# the client sent us. (this codeline is using !!rsa NOT fernet!!)
print(f"\n\nMessage: {key}\n")
print(f"\n\npublicKey: {pubKey}\n")
output = rsa.encrypt(key, pubKey)