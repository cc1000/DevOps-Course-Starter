from flask_login import UserMixin

class AppUser(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role