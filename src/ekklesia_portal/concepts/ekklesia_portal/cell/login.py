from urllib.parse import quote
from ekklesia_common.ekklesia_auth import EkklesiaAuthPathApp, EkklesiaLogin

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text

from ..login import Login


@App.cell()
class LoginCell(LayoutCell):

    _model: Login
    model_properties = ['username', 'back_url', 'from_redirect']

    def ekklesia_login_url(self):
        ekklesia_app = self._app.child(EkklesiaAuthPathApp)
        return self.link(EkklesiaLogin(back_url=self._model.back_url), app=ekklesia_app)

    def ekklesia_login_name(self):
        return self._s.ekklesia_auth.display_name

    def ekklesia_login_explanation(self):
        return customizable_text(self._request, 'ekklesia_login_explanation')

    def insecure_development_mode_enabled(self):
        return self._s.app.insecure_development_mode

    def show_internal_login(self):
        return (self.insecure_development_mode_enabled or self._model.internal_login)

    def show_ekklesia_login(self):
        return (self._s.ekklesia_auth.enabled)

    def back_url_quoted(self):
        if self._model.back_url:
            return quote(self._model.back_url)
        else:
            return None
