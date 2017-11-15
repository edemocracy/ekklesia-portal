import logging
from arguments.app import App


logg = logging.getLogger(__name__)


class TestPage:
    pass


@App.path(model=TestPage, path="test")
def test_page():
    return TestPage()
    

@App.html(model=TestPage)
def show_test_page(self, request):
    return request.app.render_template("test.j2.jade")