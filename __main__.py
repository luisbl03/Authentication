from flask import Flask
from auth import AuthService

app = Flask(__name__)
auth_service = AuthService()
app.config['service'] = auth_service