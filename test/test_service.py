import pytest
from service.service import AuthenticationService
from service.user import User


def test_addUser():
    service = AuthenticationService("users/users.db")
    id = service.addUser("root", "root", ["admin", "user"])
    assert id is not None

def test_getUser():
    service = AuthenticationService("users/users.db")
    id = service.addUser("root", "root", ["admin", "user"])
    user = service.getUser(id)
    assert user is not None
    assert user.getUsername() == "root"
    assert user.getRole() == ["admin", "user"]

def test_updateUsername():
    service = AuthenticationService("users/users.db")
    id = service.addUser("luis","luis",["admin"])
    service.updateUsername("luisito", id)
    user = service.getUser(id)
    assert user.getUsername() == "luisito"

def test_updateRole():
    service = AuthenticationService("users/users.db")
    id = service.addUser("prueba", "prueba", ["user"])
    service.updateRole(["admin", "user"], id)
    user = service.getUser(id)
    assert user.getRole() == ["admin", "user"]
def test_deleteUser():
    service = AuthenticationService("users/users.db")
    id = service.addUser("Alejandro", "Alejandro", ["user"])
    assert service.deleteUser(id) == True