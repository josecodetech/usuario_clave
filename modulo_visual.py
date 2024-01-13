import tkinter as tk
from tkinter import messagebox
from modulo_db import Database
from cryptography.fernet import Fernet
import random
import string
from modulo_cripto import obtener_clave

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title('Almacenamiento de Usuarios y Contraseñas')
        self.root.geometry('400x300')
        self.db = Database('mi_base_de_datos.db')  
              
        # self.clave_encriptacion = Fernet.generate_key()  
        self.clave_encriptacion = obtener_clave()      
        self.cipher_suite = Fernet(self.clave_encriptacion)
        
        # etiquetas y cajas textos
        lbl_id = tk.Label(root, text='ID:')
        lbl_id.grid(row=0, column=0)
        self.entry_id = tk.Entry(root)
        self.entry_id.grid(row=0, column=1)
        
        lbl_url = tk.Label(root, text='URL:')
        lbl_url.grid(row=1, column=0)
        self.entry_url = tk.Entry(root)
        self.entry_url.grid(row=1, column=1)
        
        lbl_usuario = tk.Label(root, text='Usuario:')
        lbl_usuario.grid(row=2, column=0)
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.grid(row=2, column=1)
        
        lbl_clave = tk.Label(root, text='Clave:')
        lbl_clave.grid(row=3, column=0)
        self.entry_clave = tk.Entry(root)
        self.entry_clave.grid(row=3, column=1)
        
        lbl_nota = tk.Label(root, text='Nota')
        lbl_nota.grid(row=4, column=0)
        self.entry_nota = tk.Entry(root)
        self.entry_nota.grid(row=4, column=1)
        
        # botones
        btn_grabar = tk.Button(root, text='Grabar', command=self.grabar_registro)
        btn_grabar.grid(row=5, column=0)
        
        btn_actualizar = tk.Button(root, text="Actualizar",command=self.actualizar_registro)
        btn_actualizar.grid(row=5, column=1)
        
        btn_borrar = tk.Button(root, text="Borrar",command=self.borrar_registro)
        btn_borrar.grid(row=6,column=0)
        
        btn_buscar = tk.Button(root, text="Buscar por id",command=self.buscar_por_id)
        btn_buscar.grid(row=6,column=1)
        
        btn_generar_contraseña = tk.Button(root, text='Generar contraseña',command=self.generar_contraseña)
        btn_generar_contraseña.grid(row=7,column=0, columnspan=2)
    def grabar_registro(self):
        url = self.entry_url.get()
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()
        nota = self.entry_nota.get()
        if url and usuario and clave:
            clave_encriptada =self.encriptar(clave)
            self.db.insertar_registro(url, usuario, clave_encriptada, nota)
            messagebox.showinfo('Información', 'Registro grabado correctamente')
        else:
            messagebox.showerror('Error', 'Por favor, complete todos los campos')
    def actualizar_registro(self):
        id = self.entry_id.get()
        url = self.entry_url.get()
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()
        nota = self.entry_nota.get()        
        if id and url and usuario and clave:
            clave_encriptada = self.encriptar(clave)
            self.db.actualizar_registro(id, url, usuario, clave_encriptada, nota)
            messagebox.showinfo('Información', 'Registro actualizado correctamente')
        else:
            messagebox.showerror('Error', 'Por favor, complete todos los campos')
    def borrar_registro(self):
        id = self.entry_id.get()
        if id:
            self.db.borrar_registro(id)
            messagebox.showinfo('Información', 'Registro borrado correctamente')
            self.limpiar_campos()
        else:
            messagebox.showerror('Error', 'Por favor, ingrese el ID del registro a borrar')
    def buscar_por_id(self):
        id = self.entry_id.get()
        if id:
            resultado = self.db.buscar_registro(id)
            if resultado:
                self.limpiar_campos()
                self.entry_url.insert(0, resultado[1])
                self.entry_usuario.insert(0, resultado[2])
                clave_desencriptada = self.desencriptar(resultado[3])
                self.entry_clave.insert(0, clave_desencriptada)
                self.entry_nota.insert(0, resultado[4])
            else:
                messagebox.showerror('Error', 'Registro no encontrado')
        else:
            messagebox.showerror('Error', 'Por favor, ingrese el ID del registro a buscar')
                
    def limpiar_campos(self):
        self.entry_url.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_clave.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)
    def generar_contraseña(self):
        longitud = 12
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña_generada = ''.join(random.choice(caracteres) for i in range(longitud))
        self.entry_clave.delete(0, tk.END)
        self.entry_clave.insert(0, contraseña_generada)
    def encriptar(self, texto_plano):
        texto_encriptado = self.cipher_suite.encrypt(texto_plano.encode())
        return texto_encriptado.decode()
    def desencriptar(self, texto_encriptado):
        texto_plano = self.cipher_suite.decrypt(texto_encriptado.encode())
        return texto_plano.decode()
    
