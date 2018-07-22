from ekklesia_portal.cells.layout import LayoutCell
from ekklesia_portal.collections.propositions import Propositions


class IndexCell(LayoutCell):

    def proposition_url(self):
        return self.link(Propositions())
