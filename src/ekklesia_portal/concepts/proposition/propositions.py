from ekklesia_portal.database.datamodel import Proposition
from sqlalchemy import desc
from sqlalchemy_searchable import search


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
            propositions = propositions.order_by(desc(Proposition.active_supporter_count))

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.voting_identifier, Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions
