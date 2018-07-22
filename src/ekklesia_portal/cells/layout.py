from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.views.logout import Logout
from ekklesia_portal.views.index import Index
from ekklesia_portal.collections.propositions import Propositions


class LayoutCell(Cell):

    def language(self):
        return self._request.i18n.get_locale().language

    def change_language_action(self):
        return self.link(Index(), name='change_language')

    def brand_title(self):
        return self._s.app.title

    def plain_propositions_url(self):
        return self.link(Propositions())

    def propositions_url(self, mode='sorted', tag=None):
        return self.link(Propositions(mode=mode, tag=tag))

    def login_url(self):
        from ekklesia_portal.views.login import Login
        return self.link(Login())

    def logout_action(self):
        return self.link(Logout())

    def custom_footer_url(self):
        return self._s.app.custom_footer_url

    def tos_url(self):
        return self._s.app.tos_url

    def faq_url(self):
        return self._s.app.faq_url

    def imprint_url(self):
        return self._s.app.imprint_url

    def source_code_url(self):
        return 'https://github.com/dpausp/ekklesia-portal'
