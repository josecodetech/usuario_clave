from cryptography.fernet import Fernet
import os

def obtener_clave():
    nombre_archivo = 'clave.key'
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'rb') as archivo:
            clave = archivo.read()
    else:
        clave = Fernet.generate_key()
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(clave)
    return clave