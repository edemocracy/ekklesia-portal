from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition.propositions import Propositions


class IndexCell(LayoutCell):

    template_prefix = 'ekklesia_portal'

    def proposition_url(self):
        return self.link(Propositions())
