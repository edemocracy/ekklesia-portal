from morepath import redirect

from ekklesia_portal.app import App
from .index import Index


@App.path(path='/logout')
class Logout:
    pass


@App.html(model=Logout, request_method='POST')
def logout(self, request):

    @request.after
    def forget(response):
        request.app.forget_identity(response, request)

    index_url = request.link(Index())

    if request.ekklesia_auth.authorized:
        # Redirect to the logout endpoint of the OIDC provider which then redirects back to our index page.
        logout_url = request.ekklesia_auth.logout_url(index_url)
    else:
        # Not logged in to an OIDC provider, just go back to start.
        logout_url = index_url

    return redirect(logout_url)
