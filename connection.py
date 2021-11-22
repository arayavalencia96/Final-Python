import sqlite3
import os
from tkinter import messagebox

#SI NO HAY BD DA UN AVISO
def conectar():
    try:
        if (os.path.isfile("bbdd/base_datos.db")==True):
            pass
        else:
            raise NameError
    except NameError:
        messagebox.showwarning("ERROR","Al no existir una base de datos se creo una desde 0")
 
def Database():
    global conn, cursor
    conn = sqlite3.connect('bbdd/base_datos.db')
    conn.row_factory=sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'proveedores'(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, cuit INTEGER, direccion REAL, telefono INTEGER, iva TEXT, localidad TEXT, provincia TEXT, cp INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'compra'(id INTEGER PRIMARY KEY AUTOINCREMENT, fecha BLOB, tipo_factura BLOB, forma_pago BLOB, subtotal BLOB, iva REAL, total REAL, marca TEXT, modelo BLOB)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'clientes'(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, cuit INTEGER, direccion REAL, telefono INTEGER, iva TEXT, localidad TEXT, provincia TEXT, cp INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'articulos'(id INTEGER PRIMARY KEY AUTOINCREMENT, marca BLOB, modelo BLOB, stock INTEGER, precio_costo REAL, precio_venta REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'venta'(id INTEGER PRIMARY KEY AUTOINCREMENT, fecha BLOB, tipo_factura BLOB, forma_pago BLOB, subtotal REAL, iva REAL, total REAL, marca TEXT, modelo BLOB)")
