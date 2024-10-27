from service.user import User
from service.DBManager import DBManager
from hashlib import sha256
from typing import List
import json

class AuthenticationService:
    def __init__(self, dbName:str):
        self.db = DBManager(dbName)

    def getUser(self, id:str) -> User:
        user = self.db.getUser(id)
        if user is None:
            return None
        roles = json.loads(user[3])
        return User(id=id, username=user[1], role=roles, password=user[2])
    
    def addUser(self, username:str, password:str, role:List[str]) -> str:
        hash = sha256(password.encode()).hexdigest()
        user = User(username, hash, role, None)
        if self.db.addUser(user.getID(), user.getUsername(), user.getPassword(), user.getRole()):
            return user.getID()
        else:
            return None
    
    def updateUsername(self, username:str, id:str) -> bool:
        return self.db.updateUsername(username, id)
    
    def updatePassword(self, password:str, id:str) -> bool:
        hash = sha256(password.encode()).hexdigest()
        return self.db.updatePassword(hash, id)
    
    def updateRole(self, role:List[str], id:str) -> bool:
        return self.db.updateRole(role, id)
    
    def deleteUser(self, id:str) -> bool:
        return self.db.deleteUser(id)
