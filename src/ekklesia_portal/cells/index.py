from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.collections.propositions import Propositions


class IndexCell(Cell):

    def proposition_url(self):
        return self.link(Propositions())
