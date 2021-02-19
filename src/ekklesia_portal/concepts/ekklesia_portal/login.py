from ekklesia_portal.datamodel import User
from ekklesia_portal.lib.password import password_context


class Login:

    def __init__(self, request=None, username=None, password=None, back_url=None, from_redirect=None, internal_login=None):
        self.request = request
        self.username = username
        self.password = password
        self.internal_login = internal_login
        self.back_url = back_url
        self.from_redirect = from_redirect
        self.user = None

    def find_user(self):
        if self.username is None or self.password is None:
            raise ValueError("username and/or password cannot be None")

        user = self.request.q(User).filter_by(name=self.username).scalar()
        if user is None:
            return False

        self.user = user
        return True

    def verify_password(self, insecure_empty_password_ok):
        if self.user is None:
            raise ValueError("user is not set!")
        if insecure_empty_password_ok and self.password == '':
            return True
        if self.user.password is None:
            return False

        return password_context.verify(self.password, self.user.password.hashed_password)
