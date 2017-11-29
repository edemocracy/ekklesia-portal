import logging
from markupsafe import Markup
from arguments.app import App
from arguments.helper.cell import Cell


logg = logging.getLogger(__name__)


class PageTest:
    pass


class PageTestCell(Cell):
    test_str = "test"
    test_int = 42
    test_url = "http://example.com"
    test_escaped_html = "<div>HTML from the cell (div should be escaped)</div>"
    test_html = Markup("<div>HTML from the cell (div should not be escaped)</div>")


@App.path(model=PageTest, path="pagetest")
def test_page():
    return PageTest()
    

@App.html(model=PageTest)
def show_test_page(self, request):
    return PageTestCell(self, request).show()