from morepath import redirect
from morepath import Response
from ekklesia_portal.app import App
from ekklesia_portal.cells.login import LoginCell
from ekklesia_portal.models.login import Login
import morepath


@App.path(model=Login, path="/login")
def login(request):
    if request.method == "POST":
        return Login(request, request.POST.get("username"), request.POST.get("password"))

    return Login()


@App.html(model=Login)
def show_login(self, request):
    return LoginCell(self, request).show()


@App.html(model=Login, request_method="POST")
def submit_login(self, request):
    try:
        verified = self.verify_password()
    except ValueError:
        return Response(status=400)
    if verified:
        @request.after
        def remember(response):
            identity = morepath.Identity(self.username)
            request.app.remember_identity(response, request, identity)

        return redirect("/")

    else:
        return LoginCell(self, request).show()
