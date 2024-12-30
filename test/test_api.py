"""modulos de test para la api"""
import pytest
from service.command_handlers import mock_app

@pytest.fixture(name='api_client')
def get_api():
    """fixture para obtener el cliente de la api"""

    app = mock_app()
    return app.test_client()

def test_status(api_client):
    """test para el endpoint de status"""

    response = api_client.get('/auth/v1/status')
    assert response.status_code == 204

def test_add_user(api_client):
    """test para el endpoint de add user"""

    headers = {"Content-Type": "application/json"}
    response = api_client.put('/auth/v1/user',
                           json={'username':'user', 'password':'test', 'role':'admin'},
                           headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = api_client.put('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    response = api_client.put('/auth/v1/user',
                               json={'username':'user', 'password':'test', 'role':'admin'},
                                headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = api_client.put('/auth/v1/user',
                              json={'username':'user', 'password':'test', 'role':'admin'},
                              headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = api_client.put('/auth/v1/user',
                              json={'username':'user', 'password':'test'},
                              headers=headers)
    assert response.status_code == 400

    response = api_client.put('/auth/v1/user',
                              json={'username':'user', 'password':'test', 'role':'admin'},
                              headers=headers)
    assert response.status_code == 201

    response = api_client.put('/auth/v1/user',
                              json={'username':'user', 'password':'test', 'role':'admin'},
                              headers=headers)
    assert response.status_code == 409

def test_get_user(api_client):
    """test para el endpoint de get user"""
    headers = {"Content-Type": "application/json"}
    response = api_client.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = api_client.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = api_client.get('/auth/v1/user/user', headers=headers)
    assert response.status_code == 200
    response = api_client.get('/auth/v1/user/test2', headers=headers)
    assert response.status_code == 404

def test_update_user(api_client):
    """test para el endpoint de update user"""
    headers = {"Content-Type": "application/json"}
    response = api_client.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = api_client.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 400

    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = api_client.patch('/auth/v1/user', headers=headers)
    assert response.status_code == 400

    response = api_client.patch('/auth/v1/user',
                                json={'username':'administrator', 'password':'patata'},
                                headers=headers)
    assert response.status_code == 401

    response = api_client.patch('/auth/v1/user', json={'password':'pata'}, headers=headers)
    assert response.status_code == 400

    response = api_client.patch('/auth/v1/user',
                                json={'username':'user', 'password':'patata'},
                                headers=headers)
    assert response.status_code == 200

    response = api_client.patch('/auth/v1/user',
                                json={'username':'user', 'password:':'patata','role':'admin'},
                                headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = api_client.patch('/auth/v1/user',
                                json={'username':'user', 'password':'patata','role':'admin'},
                                headers=headers)
    assert response.status_code == 200

def test_authcode(api_client):
    """test para el endpoint de authcode"""
    headers = {"Content-Type": "application/json", 'AuthToken':'token_for_admin'}
    response = api_client.get(
        '/auth/v1/auth/d6c2b61070c8cb1c60cbb7a8a026074d0a5d56a6fc5c40b2c37b26fbb3a39914', 
        headers=headers)
    assert response.status_code == 204

    response = api_client.get('/auth/v1/auth/usr', headers=headers)
    assert response.status_code == 404

def test_delete_user(api_client):
    """test para el endpoint de delete user"""
    headers = {"Content-Type": "application/json"}
    response = api_client.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 400

    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = api_client.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = api_client.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 204

    response = api_client.delete('/auth/v1/user/user', headers=headers)
    assert response.status_code == 404

    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = api_client.put('/auth/v1/user',
                              json={'username':'user2', 'password':'test', 'role':'admin'},
                              headers=headers)
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = api_client.delete('/auth/v1/user/user2', headers=headers)
    assert response.status_code == 401

    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = api_client.delete('/auth/v1/user/user2', headers=headers)
    assert response.status_code == 204
