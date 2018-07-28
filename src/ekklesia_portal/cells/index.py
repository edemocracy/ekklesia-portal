from ekklesia_portal.cells.layout import LayoutCell
from ekklesia_portal.concepts.proposition.propositions import Propositions


class IndexCell(LayoutCell):

    def proposition_url(self):
        return self.link(Propositions())
