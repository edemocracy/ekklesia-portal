from deform import Form
from ekklesia_portal.helper.utils import cached_property
from ekklesia_portal.database.datamodel import Proposition, Tag
from ekklesia_portal.schema import PropositionSchema
from ekklesia_portal.forms import PropositionForm
from sqlalchemy_searchable import search


class Propositions:
    def __init__(self, mode=None, search=None, tag=None):
        self.search = search
        self.mode = mode
        self.tag = tag

    def propositions(self, q):
        propositions = q(Proposition)

        if self.search:
            propositions = search(propositions, self.search)

        if self.tag:
            propositions = propositions.join(Tag, Proposition.tags).filter_by(tag=self.tag)

        if self.mode == "top":
            propositions = propositions.order_by(Proposition.score.desc())

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions

    def form(self, action):
        return PropositionForm(action)
