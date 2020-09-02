import morepath
from morepath import Response, redirect

from ekklesia_portal.app import App

from ..cell.login import LoginCell
from ..login import Login, UserNotFound


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
        self.find_user()
    except UserNotFound:
        return Response(status=404)
    except ValueError:
        return Response(status=400)

    if self.verify_password(insecure_empty_password_ok=request.app.settings.app.insecure_development_mode):

        @request.after
        def remember(response):
            identity = morepath.Identity(self.user.id, user=self.user)
            request.app.remember_identity(response, request, identity)

        return redirect("/")

    else:
        return LoginCell(self, request).show()
