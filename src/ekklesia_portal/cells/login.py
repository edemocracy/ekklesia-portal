from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.models.login import Login
from ekklesia_portal.ekklesia_auth import EkklesiaLogin, EkklesiaAuthPathApp


class LoginCell(Cell):
    model = Login
    model_properties = ['username']

    def ekklesia_login_url(self):
        ekklesia_app = self._app.child(EkklesiaAuthPathApp)
        return self.link(EkklesiaLogin(), app=ekklesia_app)
