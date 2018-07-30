from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.ekklesia_auth import EkklesiaLogin, EkklesiaAuthPathApp
from ..login import Login


class LoginCell(LayoutCell):
    model = Login
    model_properties = ['username']
    template_prefix = 'ekklesia_portal'

    def ekklesia_login_url(self):
        ekklesia_app = self._app.child(EkklesiaAuthPathApp)
        return self.link(EkklesiaLogin(), app=ekklesia_app)

    def insecure_development_mode_enabled(self):
        return self._app.settings.app.insecure_development_mode

    def internal_login_enabled(self):
        return self._app.settings.app.internal_login_enabled
