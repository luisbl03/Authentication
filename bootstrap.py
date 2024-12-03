import os
import sqlite3
import uuid
from hashlib import sha256

def create_database(db_path:str):
    id = str(uuid.uuid4())
    username = 'administrator'
    password = sha256('admin2024'.encode()).hexdigest()
    role = 'admin'
    authCode = sha256((username + password).encode()).hexdigest()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL, role TEXT NOT NULL, authCode TEXT NOT NULL)")
    #creamos el usuario incial
    cursor.execute("INSERT INTO users (username, password, role, authCode) VALUES (?, ?, ?, ?)", (username, password, role, authCode))
    conn.commit()
    conn.close()

def bootstrap():
    db_folder = os.getenv('STORAGE_FOLDER')
    #miramos si no existe la carpeta users
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    
    #miramos si no existe el archivo de la base de datos
    db_path = os.path.join(db_folder, 'users.db')
    if not os.path.exists(db_path):
        create_database(db_path)

if __name__ == '__main__':
    bootstrap()