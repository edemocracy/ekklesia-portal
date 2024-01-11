from ekklesia_common.cell import Cell
from ekklesia_portal.app import App
from ekklesia_portal.concepts.ballot.ballots import Ballots
from ekklesia_portal.concepts.customizable_text.customizable_texts import CustomizableTexts
from ekklesia_portal.concepts.department.departments import Departments
from ekklesia_portal.concepts.document.documents import Documents
from ekklesia_portal.concepts.page.pages import Pages
from ekklesia_portal.concepts.policy.policies import Policies
from ekklesia_portal.concepts.proposition.propositions import Propositions
from ekklesia_portal.concepts.proposition_type.proposition_types import PropositionTypes
from ekklesia_portal.concepts.subject_area.subject_areas import SubjectAreas
from ekklesia_portal.concepts.voting_phase.voting_phases import VotingPhases
from ekklesia_portal.concepts.voting_phase_type.voting_phase_types import VotingPhaseTypes
from ..admin_box import AdminBox


@App.cell()
class AdminBoxCell(Cell):

    _model: AdminBox

    def new_voting_phase_url(self):
        return self.link(VotingPhases(), '+new')

    def ballots_url(self):
        return self.link(Ballots())

    def new_ballot_url(self):
        return self.link(Ballots(), '+new')

    def pages_url(self):
        return self.link(Pages())

    def new_page_url(self):
        return self.link(Pages(), '+new')

    def policies_url(self):
        return self.link(Policies())

    def new_policy_url(self):
        return self.link(Policies(), '+new')

    def proposition_types_url(self):
        return self.link(PropositionTypes())

    def new_proposition_type_url(self):
        return self.link(PropositionTypes(), '+new')

    def propositions_url(self):
        return self.link(Propositions())

    def new_proposition_url(self):
        return self.link(Propositions(), '+new')

    def departments_url(self):
        return self.link(Departments())

    def new_department_url(self):
        return self.link(Departments(), '+new')

    def subject_areas_url(self):
        return self.link(SubjectAreas())

    def new_subject_area_url(self):
        return self.link(SubjectAreas(), '+new')

    def documents_url(self):
        return self.link(Documents())

    def new_document_url(self):
        return self.link(Documents(), '+new')

    def customizable_texts_url(self):
        return self.link(CustomizableTexts())

    def new_customizable_text_url(self):
        return self.link(CustomizableTexts(), '+new')

    def voting_phase_types_url(self):
        return self.link(VotingPhaseTypes())

    def new_voting_phase_type_url(self):
        return self.link(VotingPhaseTypes(), '+new')

    def voting_phases_url(self):
        return self.link(VotingPhases())

    def new_voting_phase_url(self):
        return self.link(VotingPhases(), '+new')
