from morepath import redirect

from ekklesia_portal.app import App


@App.path(path='/logout')
class Logout:
    pass


@App.html(model=Logout, request_method='POST')
def logout(self, request):

    @request.after
    def forget(response):
        request.app.forget_identity(response, request)

    return redirect('/')
