from typing import List, Dict
import json

class AuthService:
    def __init__(self):
        self.users = json.loads(open('../users/users.json').read())
    
    def get_user(self, id) -> Dict:
        for user in self.users:
            if user["id"] == id:
                user_json = json.dumps(user)
                return user_json
        return None
    
    def add_user(self, user: Dict) -> None:
        id = self.users[-1]["id"] + 1
        user["id"] = id
        self.users.append(user)
        with open('users/users.json', 'w') as f:
            json.dump(self.users, f)

    def delete_user(self, id) -> None:
        for user in self.users:
            if user["id"] == id:
                self.users.remove(user)
                with open('users/users.json', 'w') as f:
                    json.dump(self.users, f)
                return
    
    def update_user(self, id, user: Dict) -> None:
        for i in range(len(self.users)):
            if self.users[i]["id"] == id:
                self.users[i] = user
                with open('users/users.json', 'w') as f:
                    json.dump(self.users, f)
                return
