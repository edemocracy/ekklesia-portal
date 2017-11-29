from arguments.helper.cell import Cell
from arguments.views.propositions import Propositions
from arguments.app import App


class Index:
    pass


class IndexCell(Cell):
    @property
    def proposition_url(self):
        return self.link(Propositions())
    

@App.path(model=Index, path="")
def index():
    return Index()
    

@App.html(model=Index)
def show_index(self, request):
    return IndexCell(self, request).show()
