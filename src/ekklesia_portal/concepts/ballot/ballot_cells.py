from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell
import ekklesia_portal.concepts.voting_phase.voting_phase_helper as voting_phase_helper
from ekklesia_portal.datamodel import Ballot, Department, PropositionType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .ballot_helper import items_for_ballot_select_widgets
from .ballots import Ballots


@App.cell(Ballots)
class BallotsCell(LayoutCell):

    def ballots(self):
        return list(self._model.ballots(self._request.q))


@App.cell(Ballot)
class BallotCell(LayoutCell):

    model_properties = ['area', 'election', 'id', 'name', 'proposition_type', 'propositions', 'result', 'status', 'voting']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)

    def voting_phase_title(self):
        if self._model.voting:
            return voting_phase_helper.voting_phase_title(self._model.voting)


@App.cell(Ballot, 'edit')
class EditBallotCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        identity = self._request.identity
        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        proposition_types = self._request.q(PropositionType)
        items = items_for_ballot_select_widgets(self, departments, proposition_types)
        self._form.prepare_for_render(items)
