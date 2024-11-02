import pytest
from service.service import AuthenticationService
from service.user import User
from hashlib import sha256


def test_addUser():
    service = AuthenticationService("users/users.db")
    username = service.addUser("luis", "luis", "admin")
    assert username == "luis"

def test_getUser():
    service = AuthenticationService("users/users.db")
    username = service.addUser("root", "root", "user")
    user = service.getUser(username)
    assert user == '{"username": "root", "role": "user"}'

def test_existsAuthCode():
    service = AuthenticationService("users/users.db")
    auth_code = sha256(("luis"+"luis").encode()).hexdigest()
    assert service.existsAuthCode(auth_code) == True

def test_checkAdmin():
    service = AuthenticationService("users/users.db")
    status = service.check_admin("admin")
    assert status == True

def test_updateRole():
    service = AuthenticationService("users/users.db")
    status = service.updateRole("root", "admin")
    assert status == True

def test_updatePassword():
    service = AuthenticationService("users/users.db")
    status = service.updatePassword("root", "root")
    assert status == True

def test_deleteUser():
    service = AuthenticationService("users/users.db")
    status = service.deleteUser("root")
    assert status == True