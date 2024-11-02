import pytest_cov
import pytest
from hashlib import sha256
from service.DBManager import DBManager 

def test_insert():
    db = DBManager("users/users.db")
    assert db.addUser("luis","patata","admin") == 0

def test_exception():
    db = DBManager("users/users.db")
    assert db.addUser("luis","patata","admin") == -1

def test_get():
    db = DBManager("users/users.db")
    auth_code = sha256(("luis" + "patata").encode()).hexdigest()
    assert db.getUser("luis") == ("luis", "patata", "admin", auth_code)

def test_authCode():
    db = DBManager("users/users.db")
    auth_code = sha256(("luis" + "patata").encode()).hexdigest()
    user = db.existsAuthCode(auth_code)
    assert user == ("luis", "patata", "admin", auth_code)

def test_updatePassword():
    db = DBManager("users/users.db")
    assert db.updatePassword("admin2","luis") == True

def test_updateRole():
    db = DBManager("users/users.db")
    assert db.updateRole(username="luis",role="user") == True

def test_delete():
    db = DBManager("users/users.db")
    assert db.deleteUser("luis") == True



