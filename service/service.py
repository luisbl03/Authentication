"""modulos importados"""
from hashlib import sha256
import json
from service.user import User
from service.db_manager import DBManager

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
    def __init__(self, db_name:str):
        self.db = DBManager(db_name)

    def get_user(self, username:str) -> User:
        """Funcion que obtiene un usuario de la base de datos"""
        user = self.db.get_user(username)
        if user is None:
            raise UserNotFoundException(username)
        return json.dumps({'username': user[0], 'role': user[2]})

    def add_user(self, username:str, password:str, role:str) -> str:
        """Funcion que añade un usuario a la base de datos"""
        password_hash = sha256(password.encode()).hexdigest()
        user = User(username, password_hash, role)
        code = self.db.add_user(user.getusername(), user.getpassword(), user.getrole())
        if code== 0:
            return user.getusername(), user.getrole()
        if code == -1:
            raise UserAlreadyExists(user.getusername())
        return None,None

    def update_password(self, password:str, username:str) -> bool:
        """Funcion que actualiza la contraseña de un usuario"""
        password_hash = sha256(password.encode()).hexdigest()
        status = self.db.update_password(password_hash, username)
        if status is False:
            raise UserNotFoundException(id)

        return status

    def update_role(self, username:str ,role:str) -> bool:
        """Funcion que actualiza el rol de un usuario"""
        status = self.db.update_role(username, role)
        if status is False:
            raise UserNotFoundException(username)

        return status

    def delete_user(self, username:str) -> bool:
        """Funcion que elimina un usuario de la base de datos"""
        status = self.db.delete_user(username)
        if status is None:
            raise UserNotFoundException(username)

        return status

    def check_admin(self,role) -> bool:
        """Funcion que comprueba si un usuario tiene permisos de administrador"""
        if 'admin' not in role:
            raise Forbiden(role)
        return True

    def exists_authcode(self, authcode:str) -> str:
        """Funcion que comprueba si un codigo de autenticacion existe en la base de datos"""
        roles = self.db.exists_authcode(authcode)
        if roles is None:
            return False
        return roles
