from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.ekklesia_auth import EkklesiaLogin, EkklesiaAuthPathApp
from ..login import Login


class LoginCell(LayoutCell):
    model = Login
    model_properties = ['username']

    def ekklesia_login_url(self):
        ekklesia_app = self._app.child(EkklesiaAuthPathApp)
        return self.link(EkklesiaLogin(), app=ekklesia_app)

    def insecure_development_mode_enabled(self):
        return self._s.app.insecure_development_mode

    def show_internal_login(self):
        return (self._s.app.internal_login_enabled or self.insecure_development_mode_enabled)

    def show_ekklesia_login(self):
        return (self._s.ekklesia_auth.enabled)
