import datetime
from eliot import log_call

from ekklesia_portal.app import App

from ..cell.page_test import PageTestCell


class PageTest:
    pass


@App.path(model=PageTest, path="pagetest")
def test_page():
    return PageTest()


@App.html(model=PageTest)
def show_test_page(self, request):
    request.browser_session['old'] = request.browser_session.get('test')
    request.browser_session['test'] = datetime.datetime.now().isoformat()
    return PageTestCell(self, request).show()


class ExampleException(Exception):
    pass


@App.html(model=PageTest, name="exception")
def show_test_exception(self, request):

    @log_call
    def subsub():
        raise ExampleException("a test")

    @log_call
    def sub():
        return subsub()

    sub()
