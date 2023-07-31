from flask import current_app
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id[0].upper() + id[1:]
        self.admin = self.is_admin(id)
    def is_admin(self, id):
        users_config = current_app.config['USERS']
        for user in users_config:
            if user['username'] == id.lower():
                return user['admin']
        return False

        

                
