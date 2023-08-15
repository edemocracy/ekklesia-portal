from morepath import redirect
from ekklesia_portal.app import App


@App.path("/favicon.ico")
class FavIcon:
    pass


@App.view(model=FavIcon)
def favicon(_self, _request):
    raise redirect("/static/favicon.ico")

