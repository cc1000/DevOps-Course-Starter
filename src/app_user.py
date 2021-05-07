from flask_login import UserMixin

class AppUser(UserMixin):
    def __init__(self, username, roles):
        self.id = username
        self.roles = roles