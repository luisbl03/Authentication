from flask import Flask
from service.service import AuthenticationService
from service.authentication import auth

def run_auth():
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = AuthenticationService("users")
    app.register_blueprint(auth)
    app.run(host="0.0.0.0", port = 3000, debug=True)

