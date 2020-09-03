import morepath
from morepath import Response, redirect

from ekklesia_common.translation import _
from ekklesia_portal.app import App

from ..cell.login import LoginCell
from ..login import Login


@App.path(model=Login, path="/login")
def login(request, internal_login=False):
    if request.method == "POST":
        return Login(request, request.POST.get("username"), request.POST.get("password"))

    return Login(internal_login=internal_login)


@App.html(model=Login)
def show_login(self, request):
    return LoginCell(self, request).show()


@App.html(model=Login, request_method="POST")
def submit_login(self, request):
    try:
        user_found = self.find_user()
    except ValueError:
        return Response(status=400)

    if user_found and self.verify_password(insecure_empty_password_ok=request.app.settings.app.insecure_development_mode):

        @request.after
        def remember(response):
            identity = morepath.Identity(self.user.id, user=self.user)
            request.app.remember_identity(response, request, identity)

        request.flash(_("alert_logged_in"), "success")
        return redirect(self.back_url or "/")

    else:
        request.flash(_("alert_login_failed"), "danger")
        return LoginCell(self, request).show()
