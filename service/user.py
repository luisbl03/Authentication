from hashlib import sha256
import uuid
from typing import List

class User:
    def __init__(self, username:str, password:str, role:List[str]):
        self.__username__ = username
        self.__password__ = sha256(password.encode()).hexdigest()
        self.__role__ = role
        self.__id__ = str(uuid.uuid4())
    
    def getUsername(self) -> str:
        return self.__username__

    def getID(self) -> str:
        return self.__id__
    
    def getRole(self) -> List[str]:
        return self.__role__

    def setUserName(self, username:str) -> None:
        self.__username__ = username
    
    def setRole(self, role:List[str]) -> None:
        self.__role__ = role
    
    def setPassword(self, password:str) -> None:
        self.__password__ = sha256(password.encode()).hexdigest()