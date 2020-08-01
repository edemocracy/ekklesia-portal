from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App

from ..index import Index


@App.path(model=Index, path='')
def ekklesia_portal():
    return Index()


@App.html(model=Index)
def index(self, request):
    from ..cell.index import IndexCell
    return IndexCell(self, request).show()


@App.html(model=Index, name='change_language', request_method='POST')
def change_language(self, request):
    lang = request.POST.get('lang')
    if lang.lower() not in request.app.settings.app.languages:
        raise HTTPBadRequest()

    request.browser_session['lang'] = lang
    return redirect(request.POST.get('myurl'))
