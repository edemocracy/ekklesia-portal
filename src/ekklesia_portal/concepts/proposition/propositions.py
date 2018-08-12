from ekklesia_portal.database.datamodel import Proposition, Tag
from sqlalchemy_searchable import search
from .proposition_contracts import PropositionForm


class Propositions:
    def __init__(self, mode=None, search=None, tag=None):
        self.search = search
        self.mode = mode
        self.tag = tag

    def propositions(self, q):
        propositions = q(Proposition)

        if self.search:
            propositions = search(propositions, self.search, sort=True)

        if self.tag:
            propositions = propositions.join(*Proposition.tags.attr).filter_by(name=self.tag)

        if self.mode == "top":
            propositions = propositions.order_by(Proposition.score.desc())

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions

    def form(self, action, request):
        return PropositionForm(request, action)
