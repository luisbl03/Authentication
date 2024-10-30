import sqlite3

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
    
    def addUser(self,id:str, username:str, password:str, role:str) -> int:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)", (id, username, password, role))
        except sqlite3.IntegrityError:
            return -1
        except Exception:
            return -2
        conn.commit()
        conn.close()
        return 0
    
    def updateUser_admin(self,id:str, username:str, password:str, role:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?", (username, password, role, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updateUser(self, username:str, password:str, id:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, id))
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
