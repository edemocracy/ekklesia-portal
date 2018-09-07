from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition.propositions import Propositions


class IndexCell(LayoutCell):

    def insecure_development_mode_enabled(self):
        return self._app.settings.app.insecure_development_mode

    def new_proposition_url(self):
        return self.link(Propositions(), '+new')
