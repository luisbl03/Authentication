"""modulo List para las poner el tipo de dato de la lista"""
from typing import List

class User:
    """Clase para crear un usuario"""
    def __init__(self, username:str, password:str, role:List[str]):
        self.__username__ = username
        self.__password__ = password
        self.__role__ = role

    def getusername(self) -> str:
        """Metodo para obtener el nombre de usuario"""
        return self.__username__

    def getrole(self) -> List[str]:
        """Metodo para obtener el rol del usuario"""
        return self.__role__

    def getpassword(self) -> str:
        """Metodo para obtener la contraseña del usuario"""
        return self.__password__