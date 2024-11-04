import uuid
from typing import List

class User:
    def __init__(self, username:str, password:str, role:List[str]):
        self.__username__ = username
        self.__password__ = password
        self.__role__ = role
            
    def getUsername(self) -> str:
        return self.__username__
    
    def getRole(self) -> List[str]:
        return self.__role__
    
    def getPassword(self) -> str:
        return self.__password__