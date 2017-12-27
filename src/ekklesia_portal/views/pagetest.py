import logging
from ekklesia_portal.app import App
from ekklesia_portal.cells.pagetest import PageTestCell


logg = logging.getLogger(__name__)


class PageTest:
    pass


@App.path(model=PageTest, path="pagetest")
def test_page():
    return PageTest()


@App.html(model=PageTest)
def show_test_page(self, request):
    return PageTestCell(self, request).show()
