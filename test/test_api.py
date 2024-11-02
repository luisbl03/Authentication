import pytest
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
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.put('/auth/v1/user', headers=headers)
    assert response.status_code == 400
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 401 
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test'}, headers=headers)
    assert response.status_code == 400
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 201
    response = get_api.put('/auth/v1/user', json={'username':'test', 'password':'test', 'role':'admin'}, headers=headers)
    assert response.status_code == 409

def test_get_user(get_api):
    headers = {"Content-Type": "application/json"}
    response = get_api.get('/auth/v1/user/test', headers=headers)
    assert response.status_code == 400
    headers = {"Content-Type": "application/json","AuthToken":"test"}
    response = get_api.get('/auth/v1/user/test', headers=headers)
    assert response.status_code == 401
    headers = {"Content-Type": "application/json","AuthToken":"token_for_user"}
    response = get_api.get('/auth/v1/user/test', headers=headers)
    assert response.status_code == 200
    response = get_api.get('/auth/v1/user/test2', headers=headers)
    assert response.status_code == 404

def test_update_user(get_api):
    