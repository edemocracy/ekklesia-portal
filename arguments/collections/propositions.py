from arguments.database.datamodel import Proposition, Tag


class Propositions:
    def __init__(self, mode=None, searchterm=None, tag=None):
        self.searchterm = searchterm
        self.mode = mode
        self.tag = tag

    def propositions(self, q):
        propositions = q(Proposition)

        if self.searchterm:
            propositions = propositions.search(self.searchterm)

        if self.tag:
            propositions = propositions.join(Tag, Proposition.tags).filter_by(tag=self.tag)

        if self.mode == "top":
            propositions = propositions.order_by(Proposition.score.desc())

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions
