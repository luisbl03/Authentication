"""modulos importados"""
from hashlib import sha256
from typing import List
import json
from service.user import User
from service.DBManager import DBManager

class UserNotFoundException(Exception):
    """Excepcion que se lanza cuando no se encuentra un usuario"""
    def __init__(self, id:str):
        self.id = id

    def __str__(self):
        return f"User with id {self.id} not found"

class Forbiden(Exception):
    """Excepcion que se lanza cuando un usuario no tiene permisos para acceder a un recurso"""
    def __init__(self, role:str):
        self.role = role

    def __str__(self):
        return f"User with role {self.role} is forbiden to access this resource"

class UserAlreadyExists(Exception):
    """Excepcion que se lanza cuando se intenta añadir un usuario que ya existe"""
    def __init__(self, id:str):
        self.id = id

    def __str__(self):
        return f"User with id {self.id} already exists"

class AuthenticationService:
    """Clase que gestiona la autenticacion de los usuarios"""
    def __init__(self, dbName:str):
        self.db = DBManager(dbName)

    def getUser(self, id:str) -> User:
        """Funcion que obtiene un usuario de la base de datos"""
        user = self.db.getUser(id)
        if user is None:
            raise UserNotFoundException(id)
        return json.dumps({"id": user[0], "username": user[1], "role": user[3]})

    
    def addUser(self, username:str, password:str, role:str) -> str:
        hash = sha256(password.encode()).hexdigest()
        user = User(username, hash, role, None)
        code = self.db.addUser(user.getID(), user.getUsername(), user.getPassword(), user.getRole())
        if code== 0:
            return user.getID()
        elif code == -1:
            raise UserAlreadyExists(user.getID())
        else:
            return None
            
    
    def updateUser_admin(self, id:str, username:str, password:str, role: str) -> bool:
        hash = sha256(password.encode()).hexdigest()
        user = User(username, hash, role, id)
        return self.db.updateUser_admin(user.getID(), user.getUsername(), user.getPassword(), user.getRole())

    def updateUser(self, id:str, username:str, password:str) -> bool:
        hash = sha256(password.encode()).hexdigest()
        user = User(username, hash, None, id)
        return self.db.updateUser(user.getUsername(), user.getPassword(), user.getID()) 
    
    def deleteUser(self, id:str) -> bool:
        status = self.db.deleteUser(id)
        if status == None:
            raise UserNotFoundException(id)
        else:
            return status
    
    def check_admin(self,role) -> bool:
        if 'admin' not in role:
            raise Forbiden(role)
        return True
    
    def existsAuthCode(self, authCode:str) -> bool:
        user = self.db.existsAuthCode(authCode)
        if user is None:
            return False
        return True
