import logging
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Argument
from ekklesia_portal.cells.argument import ArgumentCell


logg = logging.getLogger(__name__)


@App.path(model=Argument, path="/arguments/{id}")
def argument(request, id):
    argument = request.q(Argument).get(id)
    return argument


@App.html(model=Argument)
def show(self, request):
    return ArgumentCell(self, request, extended=True).show()
