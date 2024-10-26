from flask import Blueprint, request, current_app, Response
from service.authentication import AuthenticationService

auth = Blueprint('auth', __name__)
root = "/auth/v1"

@auth.route(root + '/status', methods=['GET'])
def getStatus():
    return Response(status=204)