"""modulos necesarios para arrancar el servicio"""
import argparse
import os
from flask import Flask
from service.service import AuthenticationService
from service.authentication import auth



def run_auth(host:str, port:int, db_route:str):
    """arranca el servicio de autenticacion"""
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = AuthenticationService(db_route)
    app.register_blueprint(auth)
    app.run(host=host, port = port, debug=True)

def args_handler():
    """manejador de argumentos"""
    db = os.getenv('STORAGE_FOLDER')
    db_path = os.path.join(db, 'users.db')
    parser = argparse.ArgumentParser(description='Run the authentication service')
    parser.add_argument('--listening','-l', type=str,
                        default='0.0.0.0', help='Host donde se pondra a la escucha el servidor')

    parser.add_argument('--port','-p', type=int,
                        default=3001, help='Puerto donde se pondra a la escucha el servidor')

    parser.add_argument('--db', '-d', type=str, default=db_path, help='Ruta a la base de datos')
    args = parser.parse_args()
    run_auth(args.listening, args.port, args.db)

def mock_app():
    """crea una aplicacion de flask para testear"""
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = AuthenticationService('users/users.db')
    app.config['TESTING'] = True
    app.register_blueprint(auth)
    return app

if __name__ == '__main__':
    args_handler()
