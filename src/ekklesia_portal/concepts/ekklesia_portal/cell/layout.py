from ekklesia_common.cell import Cell
from ..admin_area import AdminArea
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text
from ekklesia_portal.concepts.page.pages import Pages
from ekklesia_portal.concepts.proposition.propositions import Propositions
from ekklesia_portal.concepts.voting_phase.voting_phases import VotingPhases


class LayoutCell(Cell):

    def customizable_text(self, name, lang=None):
        return customizable_text(self._request, name, lang)

    def language(self):
        return self._request.i18n.get_locale().language

    def change_language_action(self):
        from ..view.index import Index
        return self.link(Index(), name='change_language')

    def flashed_messages(self):
        try:
            return self._request.browser_session.pop("flashed_messages")
        except KeyError:
            return []

    def settings_languages(self):
        return self._app.settings.app.languages

    def favicon_url(self):
        return self.static_url('favicon.ico')

    def page_url(self):
        return self._request.url

    def search_query(self):
        return self._request.GET.get('search')

    def brand_title(self):
        return self._s.app.title

    def plain_propositions_url(self):
        return self.link(Propositions())

    def voting_phases_url(self):
        return self.link(VotingPhases())

    def pages_url(self):
        return self.link(Pages())

    def propositions_url(self):
        if (default := self._s.app.default_proposition_query):
            variables = {**default}
        else:
            variables = {}
        return self.class_link(Propositions, variables)

    def admin_area_url(self):
        return self.link(AdminArea())

    def show_admin_area(self):
        return self.current_user and self._request.identity.has_global_admin_permissions

    def show_login_button(self):
        return self._s.app.login_visible

    def login_url(self):
        from ..view.login import Login
        if self._request.path_qs != "/":
            back_url = self._request.path_qs
        else:
            back_url = None

        return self.link(Login(back_url=back_url))

    def profile_url(self):
        return self.link(self.current_user)

    def logout_action(self):
        from ..view.logout import Logout
        return self.link(Logout())

    def custom_footer_url(self):
        return self._s.app.custom_footer_url

    def tos_url(self):
        return self._s.app.tos_url

    def data_protection_url(self):
        return self._s.app.data_protection_url

    def faq_url(self):
        return self._s.app.faq_url

    def imprint_url(self):
        return self._s.app.imprint_url

    def source_code_url(self):
        return self._s.app.source_code_url
