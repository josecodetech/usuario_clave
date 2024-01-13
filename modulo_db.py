import sqlite3
from cryptography.fernet import Fernet
from modulo_cripto import obtener_clave
class Database:
    def __init__(self, nombre_base_datos):
        self.conn = sqlite3.connect(nombre_base_datos)
        self.cursor = self.conn.cursor()
        self.crear_tabla()
        # clave de encriptacion
        # self.clave_encriptacion = Fernet.generate_key() 
        self.clave_encriptacion = obtener_clave() 
        self.cipher_suite = Fernet(self.clave_encriptacion)
    def crear_tabla(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                url TEXT NOT NULL,
                                usuario TEXT NOT NULL,
                                clave TEXT NOT NULL,
                                nota TEXT
                            )
                            ''')
        self.conn.commit()
    def insertar_registro(self, url, usuario, clave, nota):
        clave_encriptada = self.encriptar(clave)
        self.cursor.execute("INSERT INTO usuarios (url, usuario, clave, nota) VALUES (?,?,?,?)", (url, usuario, clave_encriptada, nota))
        self.conn.commit()
    def actualizar_registro(self, id, url, usuario, clave, nota):
        clave_encriptada = self.encriptar(clave)
        self.cursor.execute("UPDATE usuarios SET url=?, usuario=?, clave=?, nota=? WHERE id=?", (url, usuario, clave_encriptada, nota, id))
        self.conn.commit()
    def borrar_registro(self, id):
        self.cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
        self.conn.commit()   
    def buscar_registro(self, id):
        self.cursor.execute("SELECT * FROM usuarios WHERE id=?", (id,))
        return self.cursor.fetchone() 
    def encriptar(self, texto_plano):
        texto_encriptado = self.cipher_suite.encrypt(texto_plano.encode())
        return texto_encriptado.decode()
    def desencriptar(self, texto_encriptado):
        texto_plano = self.cipher_suite.decrypt(texto_encriptado.encode())
        return texto_plano.decode()
    def cerrar_conexion(self):
        self.conn.close()
if __name__=='__main__':
    db = Database('usuarios.db')
    db.insertar_registro("jose","jose","clave","notadds")
    db.actualizar_registro(1,"jose","jddose","clave565","nsddsddsotasdafdsa")
    db.cerrar_conexion()
        
    