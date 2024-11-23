"""modulos importados"""
from hashlib import sha256
from typing import List
import json
from service.user import User
from service.DBManager import DBManager

class UserNotFoundException(Exception):
    """Excepcion que se lanza cuando no se encuentra un usuario"""
    def __init__(self, username:str):
        self.username = username

    def __str__(self):
        return f"User with username {self.username} not found"

class Forbiden(Exception):
    """Excepcion que se lanza cuando un usuario no tiene permisos para acceder a un recurso"""
    def __init__(self, role:str):
        self.role = role

    def __str__(self):
        return f"User with role {self.role} is forbiden to access this resource"

class UserAlreadyExists(Exception):
    """Excepcion que se lanza cuando se intenta añadir un usuario que ya existe"""
    def __init__(self, username:str):
        self.username = username

    def __str__(self):
        return f"User with username {self.username} already exists"

class AuthenticationService:
    """Clase que gestiona la autenticacion de los usuarios"""
    def __init__(self, dbName:str):
        self.db = DBManager(dbName)

    def getUser(self, username:str) -> User:
        """Funcion que obtiene un usuario de la base de datos"""
        user = self.db.getUser(username)
        if user is None:
            raise UserNotFoundException(username)
        return json.dumps({'username': user[0], 'role': user[2]})

    
    def addUser(self, username:str, password:str, role:str) -> str:
        hash = sha256(password.encode()).hexdigest()
        user = User(username, hash, role)
        code = self.db.addUser(user.getUsername(), user.getPassword(), user.getRole())
        if code== 0:
            return user.getUsername(), user.getRole()
        elif code == -1:
            raise UserAlreadyExists(user.getUsername())
        else:
            return None
            
    def updatePassword(self, password:str, username:str) -> bool:
        hash = sha256(password.encode()).hexdigest()
        status = self.db.updatePassword(hash, username)
        if status == False:
            raise UserNotFoundException(id)
        else:
            return status
    
    def updateRole(self, username:str ,role:str) -> bool:
        status = self.db.updateRole(username, role)
        if status == False:
            raise UserNotFoundException(username)
        else:
            return status
    
    def deleteUser(self, username:str) -> bool:
        status = self.db.deleteUser(username)
        if status == None:
            raise UserNotFoundException(username)
        else:
            return status
    
    def check_admin(self,role) -> bool:
        if 'admin' not in role:
            raise Forbiden(role)
        return True
    
    def existsAuthCode(self, authCode:str) -> str:
        roles = self.db.existsAuthCode(authCode)
        if roles is None:
            return False
        return json.dumps({'roles': roles[0]})
