"""Este modulo se encarga de manejar la base de datos"""
import sqlite3
from hashlib import sha256

class DBManager:
    """clase que maneja la base de datos"""
    def __init__(self, name:str):
        self.__dbname__ = name

    def get_user(self, username:str) -> tuple:
        """Obtiene un usuario de la base de datos"""
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        except (sqlite3.IntegrityError, sqlite3.OperationalError, sqlite3.ProgrammingError,
        sqlite3.DatabaseError,
        sqlite3.DataError, sqlite3.InterfaceError, sqlite3.NotSupportedError):
            return None
        user = cursor.fetchone()
        conn.close()
        return user

    def exists_authcode(self, authcode:str) -> str:
        """Verifica si un authCode existe en la base de datos"""
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE authCode = ?", (authcode,))
        roles= cursor.fetchone()
        conn.close()
        return roles

    def add_user(self,username:str, password:str, role:str) -> int:
        """Añade un usuario a la base de datos"""
        auth_code = sha256((username + password).encode()).hexdigest()
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role, authCode) VALUES (?, ?, ?, ?)", (username, password, role, auth_code))
        except sqlite3.IntegrityError:
            return -1
        except (sqlite3.OperationalError, sqlite3.ProgrammingError, sqlite3.DatabaseError):
            return -2
        conn.commit()
        conn.close()
        return 0
    
    def updatePassword(self, password:str, username:str) -> bool:
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        auth_code = sha256((username + password).encode()).hexdigest()
        try:
            cursor.execute("UPDATE users SET password = ?, authCode = ? WHERE username= ?", (password,auth_code, username))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updateRole(self, username:str, role:str) -> bool:
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def deleteUser(self, username:str) -> bool:
        conn = sqlite3.connect(self.__dbname__)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        except Exception as e:
            return False
        rows = cursor.rowcount
        if rows == 0:
            return None
        conn.commit()
        conn.close()
        return True
