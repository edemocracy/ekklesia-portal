import logging
from arguments.app import App


logg = logging.getLogger(__name__)


class TestPage:
    pass


@App.path(model=TestPage, path="test")
def test_page():
    return TestPage()
    

@App.view(model=TestPage)
def show_test_page(request, self):
    return "hello test"