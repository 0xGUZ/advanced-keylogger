from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("key.txt", "wb")
file.write(key)
file.close

#this script generates a Fernet key for you to use in your keylogger.py