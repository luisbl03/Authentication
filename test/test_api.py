import pytest
from hashlib import sha256
from service.command_handlers import mock_app

@pytest.fixture
def get_api():
    app = mock_app()
    return app.test_client()

def test_status(get_api):
    response = get_api.get('/auth/v1/status')
    assert response.status_code == 204

def test_add_user(get_api):
    headers = {"Content-Type": "application/json"}
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.put('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 401 
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test'}, headers=headers)
    assert response.status_code == 400
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 201
    response = get_api.put('/auth/v1/user', json={'username':'user', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 409

def test_get_user(get_api):
    headers = {"Content-Type": "application/json"}
    response = get_api.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 200
    response = get_api.get('/auth/v1/user/test2', headers=headers)
    assert response.status_code == 404

def test_update_user(get_api):
    headers = {"Content-Type": "application/json"}
    response = get_api.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    response = get_api.patch('/auth/v1/user', json={'username':'administrator', 'password':'patata'}, headers=headers)
    assert response.status_code == 401
    response = get_api.patch('/auth/v1/user', json={'password':'pata'}, headers=headers)
    assert response.status_code == 400
    response = get_api.patch('/auth/v1/user', json={'username':'user', 'password':'patata'}, headers=headers)
    assert response.status_code == 200
    response = get_api.patch('/auth/v1/user', json={'username':'user', 'password:':'patata','role':'admin'}, headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = get_api.patch('/auth/v1/user', json={'username':'user', 'password':'patata','role':'admin'}, headers=headers)
    assert response.status_code == 200

def test_authcode(get_api):
    headers = {"Content-Type": "application/json", 'AuthToken':'token_for_admin'}
    password_sha = sha256('patata'.encode()).hexdigest()
    authCode = sha256(('user'+password_sha).encode()).hexdigest()
    response = get_api.get('/auth/v1/auth/d6c2b61070c8cb1c60cbb7a8a026074d0a5d56a6fc5c40b2c37b26fbb3a39914', headers=headers)
    assert response.status_code == 204
    response = get_api.get('/auth/v1/auth/usr', headers=headers)
    assert response.status_code == 404

def test_delete_user(get_api):
    headers = {"Content-Type": "application/json"}
    response = get_api.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 204
    response = get_api.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 404
    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = get_api.put('/auth/v1/user', json={'username':'user2', 'password':'test', 'role':'admin'}, headers=headers)
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.delete('/auth/v1/user/user2', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = get_api.delete('/auth/v1/user/user2', headers=headers)
    assert response.status_code == 204