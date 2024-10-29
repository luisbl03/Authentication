"""Importaciones"""
from flask import Blueprint, request, current_app, Response
from service.service import UserNotFoundException, Forbiden, UserAlreadyExists, AuthenticationService
import requests

auth = Blueprint('auth', __name__)
ROOT = "/auth/v1"

@auth.route(ROOT + '/status', methods=['GET'])
def get_status() -> Response:
    """Funcion que devuelve el estado del servicio"""
    return Response(status=204)

@auth.route(ROOT + '/user', methods=['PUT'])
def add_user() -> Response:
    """Funcion que añade un usuario a la base de datos"""
    service = AuthenticationService(current_app.config['service'])
    headers = request.headers
    #miramos si esta la cabecera de autorizacion
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}', 
                        status=400, content_type='application/json')
    #miramos si el token es valido, para ello debemos consultar al servicio de token
    token = headers['AuthToken']
    response = requests.get(f'http://localhost:3002/api/v1/token/{token}', timeout=20)
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
        id = service.addUser(request.json['username'], request.json['password'], request.json['role'])
    except UserAlreadyExists:
        return Response(response='{"error": "User already exists"}',
                        status=409, content_type='application/json')
    if id is None:
        return Response(response='{"error": "Internal server error"}',
                        status=500, content_type='application/json')
    return Response(response=f'{{"id": "{id}"}}', status=201, content_type='application/json')


@auth.route(ROOT + '/user/<id>', methods=['GET'])
def get_user(id:str):
    """funcion para obtener el usuario con el id dado"""
    service = current_app.config['service']
    headers = request.headers
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}',
                        status=400, content_type='application/json')
    token = headers['AuthToken']
    response = requests.get(f'http://localhost:3002/api/v1/token/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    #obtenemos el usuario
    try:
        user = service.getUser(id)
        return Response(response=user, status=200, content_type='application/json')
    except UserNotFoundException:
        return Response(response='{"error": "User not found"}',
                        status=404, content_type='application/json')

@auth.route(ROOT + '/user/<id>', methods=['DELETE'])
def delete_user(id:str):
    service = current_app.config['service']
    headers = request.headers
    if 'AuthToken' not in headers:
        return Response(response='{"error": "No AuthToken header"}',
                        status=400, content_type='application/json')
    token = headers['AuthToken']
    response = requests.get(f'http://localhost:3002/api/v1/token/{token}', timeout=20)
    if response.status_code != 200:
        return Response(response='{"error": "Invalid token"}',
                        status=401, content_type='application/json')
    status = ''
    try:
        status = service.deleteUser(id)
    except UserNotFoundException:
        return Response(response='{"error": "User not found"}',
                        status=404, content_type='application/json')
    if status:
        return Response(status=204)
    else:
        return Response(response='{"error": "Internal server error"}',
                        status=500, content_type='application/json')

@auth.route(ROOT + '/user/<id>', methods=['POST', 'PATCH'])
def update_user(id:str):
    pass

@auth.route(ROOT + "/auth/<auth_code>", methods=['GET'])
def auth_user(auth_code):
    pass