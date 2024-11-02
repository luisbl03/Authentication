from flask import Flask
from service.service import AuthenticationService
from service.authentication import auth
import argparse


def run_auth(host:str, port:int, db_route:str):
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = AuthenticationService(db_route)
    app.register_blueprint(auth)
    app.run(host=host, port = port, debug=True)

def args_handler():
    parser = argparse.ArgumentParser(description='Run the authentication service')
    parser.add_argument('--listening','-l', type=str, default='0.0.0.0', help='Host donde se pondra a la escucha el servidor')
    parser.add_argument('--port','-p', type=int, default=3000, help='Puerto donde se pondra a la escucha el servidor')
    parser.add_argument('--db', '-d', type=str, default='users/users.db', help='Ruta a la base de datos')
    args = parser.parse_args()
    run_auth(args.listening, args.port, args.db)

def mock_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = AuthenticationService('users/users.db')
    app.config['TESTING'] = True
    app.register_blueprint(auth)
    return app

