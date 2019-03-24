from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition.propositions import Propositions
from ekklesia_portal.concepts.department.departments import Departments
from ekklesia_portal.concepts.voting_phase.voting_phases import VotingPhases
from ekklesia_portal.concepts.ballot.ballots import Ballots
from ekklesia_portal.concepts.policy.policies import Policies
from ekklesia_portal.concepts.proposition_type.proposition_types import PropositionTypes


class IndexCell(LayoutCell):

    def insecure_development_mode_enabled(self):
        return self._app.settings.app.insecure_development_mode

    def new_proposition_url(self):
        return self.link(Propositions(), '+new')

    def new_voting_phase_url(self):
        return self.link(VotingPhases(), '+new')

    def ballots_url(self):
        return self.link(Ballots())

    def policies_url(self):
        return self.link(Policies())

    def proposition_types_url(self):
        return self.link(PropositionTypes())

    def departments_url(self):
        return self.link(Departments())
