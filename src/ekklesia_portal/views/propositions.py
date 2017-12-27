from ekklesia_portal.app import App
from ekklesia_portal.cells.propositions import PropositionsCell
from ekklesia_portal.collections.propositions import Propositions


@App.path(model=Propositions, path='propositions')
def propositions(request, searchterm, tag, mode="sorted"):
    return Propositions(mode, searchterm, tag)


@App.html(model=Propositions)
def propositions_html(self, request):
    return PropositionsCell(self, request, layout=True).show()
