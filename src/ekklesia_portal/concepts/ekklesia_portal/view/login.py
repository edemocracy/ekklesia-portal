from urllib.parse import unquote
import morepath
from morepath import Request, Response, redirect
from webob.exc import HTTPForbidden

from ekklesia_common.translation import _
from ekklesia_portal.app import App

from ..cell.login import LoginCell
from ..login import Login


def unquote_or_none(url):
    if url is None:
        return url
    else:
        return unquote(url)


@App.path(model=Login, path="/login")
def login(request, internal_login=False, back_url=None, from_redirect=False):
    if request.method == "POST":
        params = request.POST

        return Login(request, params.get("username"), params.get("password"), unquote_or_none(params.get("back_url")))

    return Login(back_url=unquote_or_none(back_url), from_redirect=from_redirect, internal_login=internal_login)


@App.html(model=Login)
def show_login(self, request):
    return LoginCell(self, request).show()


@App.html(model=Login, request_method="POST")
def submit_login(self, request):
    try:
        user_found = self.find_user()
    except ValueError:
        return Response(status=400)

    is_insecure_empty_password_ok = request.app.settings.app.insecure_development_mode

    if user_found and self.verify_password(is_insecure_empty_password_ok):

        @request.after
        def remember(response):
            identity = morepath.Identity(self.user.id, user=self.user)
            request.app.remember_identity(response, request, identity)

        request.flash(_("alert_logged_in"), "success")
        return redirect(self.back_url or "/")

    else:
        request.flash(_("alert_login_failed"), "danger")
        return LoginCell(self, request).show()


@App.html(model=HTTPForbidden)
def redirect_to_login(self, request: Request):
    if request.current_user:
        return self

    return redirect(request.link(Login(back_url=request.path_qs, from_redirect=1)))
