import sqlite3
from hashlib import sha256

class DBManager:
    def __init__(self, name:str):
        self.__dbName__ = name
    
    def getUser(self, id) -> tuple:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        except Exception as e:
            return None
        user = cursor.fetchone()
        conn.close()
        return user
    
    def existsAuthCode(self, authCode:str) -> str:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE authCode = ?", (authCode,))
        user = cursor.fetchone()
        conn.close()
        return user 
    
    def addUser(self,id:str, username:str, password:str, role:str) -> int:
        auth_code = sha256((username + password).encode()).hexdigest()
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (id, username, password, role, authCode) VALUES (?, ?, ?, ?, ?)", (id, username, password, role, auth_code))
        except sqlite3.IntegrityError:
            return -1
        except Exception:
            return -2
        conn.commit()
        conn.close()
        return 0
    
    def updateUsername(self, id:str, username:str, password:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        auth_code = sha256((username + password).encode()).hexdigest()
        try:
            cursor.execute("UPDATE users SET username = ?, authCode = ? WHERE id = ?", (username,auth_code, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updatePassword(self, id:str, password:str, username:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        auth_code = sha256((username + password).encode()).hexdigest()
        try:
            cursor.execute("UPDATE users SET password = ?, authCode = ? WHERE id = ?", (password,auth_code, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updateRole(self, id:str, role:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def deleteUser(self, id:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        except Exception as e:
            return False
        rows = cursor.rowcount
        if rows == 0:
            return None
        conn.commit()
        conn.close()
        return True
