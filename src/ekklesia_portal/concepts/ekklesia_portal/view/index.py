from urllib.parse import urlparse
from eliot import log_message
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
    if lang not in request.app.settings.app.languages:
        raise HTTPBadRequest("unsupported language")

    back_url = request.POST.get('back_url')
    parsed_app_url = urlparse(request.application_url)
    parsed_back_url = urlparse(back_url)

    if parsed_app_url.netloc != parsed_back_url.netloc:
        log_message(message_type="invalid_redirect", url=back_url)
        raise HTTPBadRequest("redirect not allowed")

    request.browser_session['lang'] = lang
    return redirect(back_url)
