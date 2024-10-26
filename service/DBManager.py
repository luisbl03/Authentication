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
    
    def addUser(self,id:str, username:str, password:str, role:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)", (id, username, password, role))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updateUsername(self,username:str, id:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updatePassword(self,password:str, id:str) -> bool:
        conn = sqlite3.connect(self.__dbName__)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password, id))
        except Exception as e:
            return False
        conn.commit()
        conn.close()
        return True
    
    def updateRole(self,role:str, id:str) -> bool:
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
        conn.commit()
        conn.close()
        return True
