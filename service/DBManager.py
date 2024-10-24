import sqlite3

class DBManager:
    def __init__(self, name:str):
        self.dbName = name