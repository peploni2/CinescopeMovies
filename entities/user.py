from clients.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, roles: list, api_manager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api_manager

    @property
    def creds(self):
        return self.email, self.password