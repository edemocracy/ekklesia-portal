from ekklesia_portal.app import App
from ekklesia_portal.cells.index import IndexCell


class Index:
    pass


@App.path(model=Index, path="")
def index():
    return Index()


@App.html(model=Index)
def show_index(self, request):
    return IndexCell(self, request).show()
