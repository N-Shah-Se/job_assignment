from cryptography.fernet import Fernet
import base64
with open('secrestkey.key', 'rb') as filekey:
    key = filekey.read()
 
# using the generated key
print(key)
# key = str(key).split("'")[1]
fernet = Fernet(key)

encrypted = ''

with open('encrypted.txt', 'rb') as filekey:
    tokens = filekey.read()
decrypted = fernet.decrypt(tokens)

print(decrypted)