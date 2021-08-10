import datetime
import logging

from ekklesia_portal.app import App

from ..cell.page_test import PageTestCell

logg = logging.getLogger(__name__)


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


@App.path(path="pagetest/exception")
class PageTestException:
    pass


class ExampleException(Exception):
    pass


@App.html(model=PageTestException)
def show_test_exception(self, request):
    raise ExampleException("a test")
