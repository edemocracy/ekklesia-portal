import logging
from arguments.app import App
from arguments.cells.pagetest import PageTestCell


logg = logging.getLogger(__name__)


class PageTest:
    pass


@App.path(model=PageTest, path="pagetest")
def test_page():
    return PageTest()


@App.html(model=PageTest)
def show_test_page(self, request):
    return PageTestCell(self, request).show()
