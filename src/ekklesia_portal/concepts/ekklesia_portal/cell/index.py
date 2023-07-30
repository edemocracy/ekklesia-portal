from ekklesia_portal.concepts.ekklesia_portal.admin_box import AdminBox
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition.propositions import Propositions
from ekklesia_portal.datamodel import Page, VotingPhase
from ekklesia_portal.enums import VotingStatus


class IndexCell(LayoutCell):

    def scheduled_voting_phases(self):
        return (self._request.q(VotingPhase).
            where(VotingPhase.target is not None).
            where(VotingPhase.status.in_([VotingStatus.PREPARING, VotingStatus.VOTING])).
            order_by(VotingPhase.target))

    def insecure_development_mode_enabled(self):
        return self._app.settings.app.insecure_development_mode

    def new_proposition_url(self):
        return self.link(Propositions(), '+new')

    def welcome_text(self):
        return (
            self._request.q(Page.text).filter_by(name='content_welcome', lang=self.language).scalar()
            or 'add your welcome page!'
        )

    def admin_box(self):
        return AdminBox()
