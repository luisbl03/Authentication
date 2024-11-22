import sqlite3
from hashlib import sha256

class DBManager:
    def __init__(self, name:str):
        self.__dbName__ = name
    
    def getUser(self, username:str) -> tuple:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        except Exception as e:
            return None
        user = cursor.fetchone()
        conn.close()
        return user
    
    def existsAuthCode(self, authCode:str) -> str:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE authCode = ?", (authCode,))
        roles= cursor.fetchone()
        conn.close()
        return roles
    
    def addUser(self,username:str, password:str, role:str) -> int:
        auth_code = sha256((username + password).encode()).hexdigest()
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role, authCode) VALUES (?, ?, ?, ?)", (username, password, role, auth_code))
        except sqlite3.IntegrityError:
            return -1
        except Exception:
            return -2
        conn.commit()
        conn.close()
        return 0
    
    def updatePassword(self, password:str, username:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
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
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def deleteUser(self, username:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
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
