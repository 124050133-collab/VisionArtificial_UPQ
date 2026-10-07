import sqlite3
import numpy as np
import cv2
import json

def conectar_db(db_name="sistema_vision.db"):
   
    return sqlite3.connect(db_name)

def inicializar_bd():
   
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    
    # Tabla de imágenes con arreglo de píxeles en formato JSON
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagenes_procesadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_imagen TEXT,
            tipo_proceso TEXT,
            ancho INTEGER,
            alto INTEGER,
            pixeles_json TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def registrar_usuario(nombre, ap_pat, ap_mat, usuario, contrasena):
    
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido_paterno, apellido_materno, usuario, contrasena)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, ap_pat, ap_mat, usuario, contrasena))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # El nombre de usuario ya existe

def validar_login(usuario, contrasena):
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?
    ''', (usuario, contrasena))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def guardar_imagen_pixeles(ruta_o_matriz, tipo_proceso="Original"):
    
    if isinstance(ruta_o_matriz, str):
        imagen_bgr = cv2.imread(ruta_o_matriz)
    else:
        imagen_bgr = ruta_o_matriz

    if imagen_bgr is None:
        return False

    # Convertir BGR (OpenCV) a RGB
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    
    alto, ancho, _ = imagen_rgb.shape
    
    # Aplanar la matriz a una lista de listas [[R, G, B], [R, G, B], ...]
    pixeles_lista = imagen_rgb.reshape(-1, 3).tolist()
    
    # Convertir a cadena de texto formato JSON
    pixeles_json = json.dumps(pixeles_lista)
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imagenes_procesadas (nombre_imagen, tipo_proceso, ancho, alto, pixeles_json)
        VALUES (?, ?, ?, ?, ?)
    ''', ("foto_capturada", tipo_proceso, ancho, alto, pixeles_json))
    
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    # Inicializar la base de datos al ejecutar directamente este script
    inicializar_bd()
    print("Base de datos inicializada correctamente.")