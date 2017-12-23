from arguments.database.datamodel import User
from arguments.lib.password import password_context


class Login:
    def __init__(self, request=None, username=None, password=None):
        self.request = request
        self.username = username
        self.password = password

    def verify_password(self):

        if self.username is None or self.password is None:
            raise ValueError("username and/or password cannot be None")

        user = self.request.q(User).filter_by(name=self.username).scalar()
        if user is None or user.password is None:
            return False

        return password_context.verify(self.password, user.password.hashed_password)
