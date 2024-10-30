import os
import sqlite3
import uuid
from hashlib import sha256

def create_database():
    id = str(uuid.uuid4())
    username = 'administrator'
    password = sha256('admin2024'.encode()).hexdigest()
    role = 'admin'
    authCode = sha256((username + password).encode()).hexdigest()

    conn = sqlite3.connect('users/users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id TEXT NOT NULL, username TEXT PRIMARY KEY, password TEXT NOT NULL, role TEXT NOT NULL, authCode TEXT NOT NULL)")
    #creamos el usuario incial
    cursor.execute("INSERT INTO users (id, username, password, role, authCode) VALUES (?, ?, ?, ?, ?)", (id, username, password, role, authCode))
    conn.commit()
    conn.close()

def bootstrap():
    #miramos si no existe la carpeta users
    if not os.path.exists('users'):
        os.makedirs('users')
    
    #miramos si no existe el archivo de la base de datos
    if not os.path.exists('users/users.db'):
        create_database()

if __name__ == '__main__':
    bootstrap()