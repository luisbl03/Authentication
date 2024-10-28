from flask import Blueprint, request, current_app, Response
from service.service import AuthenticationService, UserNotFoundException, Forbiden

auth = Blueprint('auth', __name__)
root = "/auth/v1"

@auth.route(root + '/status', methods=['GET'])
def getStatus():
    return Response(status=204)

@auth.route(root + '/user', methods=['PUT'])
def add_user():
    pass

@auth.route(root + '/user/<id>', methods=['GET'])
def get_user(id):
    pass

@auth.route(root + '/user/<id>', methods=['DELETE'])
def delete_user(id):
    pass

@auth.route(root + '/user/<id>', methods=['POST', 'PATCH'])
def update_user(id):
    pass

@auth.route(root + "/auth/<auth_code>", methods=['GET'])
def auth_user(auth_code):
    pass