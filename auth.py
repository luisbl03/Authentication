from typing import List, Dict
import json

class AuthService:
    def __init__(self):
        self.users = json.loads(open('users/users.json').read())