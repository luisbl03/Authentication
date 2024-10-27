import pytest_cov
import pytest
from service.DBManager import DBManager 

def test_insert():
    db = DBManager("users/users.db")
    assert db.addUser(1,"root","root","admin") == True

def test_exception():
    db = DBManager("users/users.db")
    assert db.addUser(1,"root","root","admin") == False

def test_get():
    db = DBManager("users/users.db")
    assert db.getUser(1) == ("1","root","root",'"admin"')

def test_updateUsername():
    db = DBManager("users/users.db")
    assert db.updateUsername("admin","1") == True

def test_updatePassword():
    db = DBManager("users/users.db")
    assert db.updatePassword("admin2",1) == True

def test_updateRole():
    db = DBManager("users/users.db")
    assert db.updateRole(["admin", "user"],1) == True

def test_delete():
    db = DBManager("users/users.db")
    assert db.deleteUser(1) == True

