"""Importaciones"""
#import os
from typing import List
import requests
from flask import Blueprint, request, current_app, Response
from service.service import UserNotFoundException, Forbiden, UserAlreadyExists


auth = Blueprint('auth', __name__)
ROOT = "/auth/v1"
TOKEN_ENDPOINT = "http://192.168.0.7:3002/api/v1/token"

@auth.route(ROOT + '/status', methods=['GET'])
def get_status() -> Response:
    """entrypoint que devuelve el estado del servicio"""
    return Response(status=204)

@auth.route(ROOT + '/user', methods=['PUT'])
def add_user() -> Response:
    """entrypoint que agrega un usuario"""
    body = request.get_json()
    #validacion del cuerpo de la request
    valid = check_body(body)
    if not valid:
        return Response(status=400, response="Bad Request, missing parameters (username, password)")
    #validacion de la cabecera de autenticacion
    roles = check_auth_header(request.headers)
    if roles is None:
        return Response(status=401, response="Unauthorized")
    #validacion de los roles
    valid = check_roles(roles)
    if not valid:
        return Response(status=401, response="Forbidden")
    #agregar usuario
    service = current_app.config['service']
    try:
        username, role = service.add_user(request.json['username'],
        request.json['password'], request.json['role'])
    except (UserAlreadyExists,KeyError, Forbiden)as e:
        return Response(status=409, response=str(e))
    if username is None:
        return Response(response='{"error": "Internal server error"}',
                        status=500, content_type='application/json')
    return Response(response=f'{{"username": "{username}", "roles": "{role}"}}',
    status=201, content_type='application/json')

@auth.route(ROOT + '/user/<username>', methods=['GET'])
def get_user(username:str) -> Response:
    """entrypoint que obtiene un usuario"""
    #validacion de la cabecera de autenticacion
    roles = check_auth_header(request.headers)
    if roles is None:
        return Response(status=401, response="Unauthorized")
    #obtener usuario
    service = current_app.config['service']
    try:
        user = service.get_user(username)
    except UserNotFoundException as e:
        return Response(status=404, response=str(e))
    return Response(response=user, status=200, content_type='application/json')

@auth.route(ROOT + '/user/<username>', methods=['DELETE'])
def delete_user(username:str) -> Response:
    """entrypoint que elimina un usuario"""
    #validacion de la cabecera de autenticacion
    roles = check_auth_header(request.headers)
    if roles is None:
        return Response(status=401, response="Unauthorized")
    #validacion de los roles
    valid = check_roles(roles)
    if not valid:
        #miramos si el usuario que esta borrando es el suyo
        if username != get_usertoken(request.headers):
            return Response(status=401, response="Unauthorized")
    #eliminar usuario
    service = current_app.config['service']
    try:
        status = service.delete_user(username)
    except UserNotFoundException as e:
        return Response(status=404, response=str(e))
    if status:
        return Response(status=204)
    return Response(response='{"error": "Internal server error"}',
                    status=500, content_type='application/json')

@auth.route(ROOT + '/user/<username>', methods=['PATCH', 'POST'])
def update_user(username:str) -> Response:
    """entrypoint que actualiza un usuario"""
    #validacion de la cabecera de autenticacion
    roles = check_auth_header(request.headers)
    if roles is None:
        return Response(status=401, response="Unauthorized")
    #validacion del cuerpo de la request
    body = request.get_json()
    valid = check_body(body)
    if not valid:
        return Response(status=400, response="Bad Request, missing parameters (username, password)")
    #validacion de los roles
    valid = check_roles(roles)
    username = request.json['username']
    if not valid:
        #solo tiene permiso para tocar su usuario
        if username != get_usertoken(request.headers):
            return Response(status=401, response="Unauthorized")
    #actualizar usuario
    service = current_app.config['service']
    try:
        status_pass = service.update_password(request.json['password'], username)
    except UserNotFoundException as e:
        return Response(status=404, response=str(e))

    status_role = True
    #miramos si hay rol en la request
    if 'role' in request.json:
        try:
            status_role = service.update_role(username, request.json['role'])
        except UserNotFoundException as e:
            return Response(status=404, response=str(e))
    if status_pass and status_role:
        user = service.get_user(username)
        return Response(status=200, response=user, content_type='application/json')
    return Response(response='{"error": "Internal server error"}',
                    status=500, content_type='application/json')

@auth.route(ROOT + '/is_authorized/<auth_code>', methods=['GET'])
def is_authorized(auth_code:str) -> Response:
    """entrypoint que comprueba si un codigo de autenticacion existe en la base de datos"""
    service = current_app.config['service']
    roles = service.exists_authcode(auth_code)
    if roles is False:
        return Response(status=404)
    return Response(response=f'{{"roles": "{roles}"}}', status=200, content_type='application/json')


def check_body(body: dict) -> bool:
    """Función que valida el cuerpo de la petición"""
    if 'username' in body and 'password' in body and 'role' in body:
        return True
    return False

def check_auth_header(headers) -> List[str]:
    """Función que valida la cabecera de autenticación"""
    if not "AuthToken" in headers:
        return None
    token = headers['AuthToken']
    response = requests.get(f'{TOKEN_ENDPOINT}/{token}', timeout=20)
    if response.status_code == 200:
        return response.json()['roles']
    return None

def check_roles(roles: List[str]) -> bool:
    """Funcion que mira si es administrado el usuario"""
    if 'admin' in roles:
        return True
    return False

def get_usertoken(headers) -> str:
    """Funcion que obtiene el usuario del token de autenticacion"""
    token = headers['AuthToken']
    response = requests.get(f'{TOKEN_ENDPOINT}/{token}', timeout=20)
    if response.status_code == 200:
        return response.json()['username']
    return None
