from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.views.logout import Logout
from ekklesia_portal.collections.propositions import Propositions


class LayoutCell(Cell):

    def plain_propositions_url(self):
        return self.link(Propositions())

    def propositions_url(self, mode='sorted', tag=None):
        return self.link(Propositions(mode=mode, tag=tag))

    def login_url(self):
        from ekklesia_portal.views.login import Login
        return self.link(Login())

    def logout_action(self):
        return self.link(Logout())
