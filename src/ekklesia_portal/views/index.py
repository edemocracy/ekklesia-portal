from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App


@App.path(path='')
class Index:
    pass


@App.html(model=Index)
def show(self, request):
    from ekklesia_portal.cells.index import IndexCell
    return IndexCell(self, request).show()


@App.html(model=Index, name='change_language', request_method='POST')
def change_language(self, request):
    lang = request.POST.get('lang')
    if lang not in ('de', 'en', 'fr'):
        raise HTTPBadRequest()

    request.browser_session['lang'] = lang
    return redirect('/')
