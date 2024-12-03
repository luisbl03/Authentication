"""Importaciones"""
from flask import Blueprint, request, current_app, Response
from service import UserNotFoundException, Forbiden, UserAlreadyExists, AuthenticationService
import requests
import os

auth = Blueprint('auth', __name__)
ROOT = "/auth/v1"
token_endpoint = os.getenv('token_endpoint')

@auth.route(ROOT + '/status', methods=['GET'])
def get_status() -> Response:
    """Funcion que devuelve el estado del servicio"""
    return Response(status=204)

@auth.route(ROOT + '/user', methods=['PUT'])
def add_user() -> Response:
    """Funcion que añade un usuario a la base de datos"""
    service = current_app.config['service']
    headers = request.headers
    #miramos si esta la cabecera de autorizacion
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}', 
                        status=400, content_type='application/json')
    if not request.json:
        return Response(response='{"error": "No json body"}',status=400, content_type='application/json')
    
    #miramos si el token es valido, para ello debemos consultar al servicio de token
    token = headers['AuthToken']
    response = requests.get(f'{token_endpoint}/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    #miramos si el token es de administrador
    roles = response.json()['roles']
    try:
        if service.check_admin(roles):
            pass
    except Forbiden:
        return Response(response='{"error": "Forbiden"}',
                        status=401, content_type='application/json')
    #añadimos el usuario
    try:
        username, role = service.addUser(request.json['username'], request.json['password'], request.json['role'])
    except UserAlreadyExists:
        return Response(response='{"error": "User already exists"}',
                        status=409, content_type='application/json')
    except KeyError:
        return Response(response='{"error": "Invalid json body","expected": ["username", "password", "role"]}',
                        status=400, content_type='application/json')
    if username is None:
        return Response(response='{"error": "Internal server error"}',
                        status=500, content_type='application/json')
    return Response(response=f'{{"username": "{username}", "roles": "{role}"}}', status=201, content_type='application/json')


@auth.route(ROOT + '/user/<username>', methods=['GET'])
def get_user(username:str):
    """funcion para obtener el usuario con el id dado"""
    service = current_app.config['service']
    headers = request.headers
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}',
                        status=400, content_type='application/json')
    token = headers['AuthToken']
    response = requests.get(f'{token_endpoint}/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    #obtenemos el usuario
    try:
        user = service.getUser(username)
        return Response(response=user, status=200, content_type='application/json')
    except UserNotFoundException:
        return Response(response='{"error": "User not found"}',
                        status=404, content_type='application/json')

@auth.route(ROOT + '/user/<username>', methods=['DELETE'])
def delete_user(username:str):
    service = current_app.config['service']
    headers = request.headers
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}',
                        status=400, content_type='application/json')
    token = headers['AuthToken']
    response = requests.get(f'{token_endpoint}/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    userToken = response.json()['username']
    roles = response.json()['roles']
    if not 'admin' in roles:
        if username != userToken:
            return Response(response='{"error": "Forbiden"}',
                            status=401, content_type='application/json')
    status = ''
    try:
        status = service.deleteUser(username)
    except UserNotFoundException:
        return Response(response='{"error": "User not found"}',
                        status=404, content_type='application/json')
    if status:
        return Response(status=204)
    else:
        return Response(response='{"error": "Internal server error"}',
                        status=500, content_type='application/json')

@auth.route(ROOT + '/user', methods=['POST', 'PATCH'])
def update_user():
    service = current_app.config['service']
    headers = request.headers
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}',
                        status=400, content_type='application/json')
    
    if not request.json:
        return Response(response='{"error": "No json body"}',status=400, content_type='application/json')
    token = headers['AuthToken']
    response = requests.get(f'{token_endpoint}/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    roles = response.json()['roles']
    userToken = response.json()['username']
    if not 'admin' in roles:
        try:
            username = request.json['username']
        except KeyError:
            return Response(response='{"error": "Invalid json body","expected": ["username"]}',
                            status=400, content_type='application/json')
        if username != userToken:
            return Response(response='{"error": "Forbiden"}',
                            status=401, content_type='application/json')
        try:
            user = service.getUser(userToken)
        except UserNotFoundException:
            return Response(response='{"error": "User not found"}',
                            status=404, content_type='application/json')
        if "password" in request.json:
            status = service.updatePassword(request.json['password'], userToken)
            if not status:
                return Response(response='{"error": "Internal server error"}',
                                status=500, content_type='application/json')
        if 'role' in request.json:
            return Response(response='{"error": "Forbiden"}',
                            status=401, content_type='application/json')
        user = service.getUser(userToken)
        return Response(status=200, response=user, content_type='application/json')
    else:
        username = request.json['username']
        if "role" in request.json:
            status = service.updateRole(username, request.json['role'])
            if not status:
                return Response(response='{"error": "Internal server error"}',
                                status=500, content_type='application/json')
        if "password" in request.json:
            status = service.updatePassword(request.json['password'], username)
            if not status:
                return Response(response='{"error": "Internal server error"}',
                                status=500, content_type='application/json')
        user = service.getUser(username)
        return Response(status=200, response=user, content_type='application/json')
            
@auth.route(ROOT + "/auth/<auth_code>", methods=['GET'])
def auth_user(auth_code:str):
    service = current_app.config['service']
    roles = service.existsAuthCode(auth_code)
    if roles is None:
        return Response(response='{"error": "User not found"}',
                        status=404, content_type='application/json')
    return Response(response=roles, status=200, content_type='application/json')