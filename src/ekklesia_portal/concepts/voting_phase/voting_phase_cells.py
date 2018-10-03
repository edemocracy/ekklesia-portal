from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.database.datamodel import VotingPhase, VotingPhaseType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phases import VotingPhases
from .voting_phase_contracts import VotingPhaseForm
from .voting_phase_helper import items_for_voting_phase_select_widgets


class VotingPhasesCell(LayoutCell):
    model = VotingPhases

    def voting_phases(self):
        return list(self._model.voting_phases(self._request.q))

    def show_new_button(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)


class VotingPhaseCell(LayoutCell):
    model = VotingPhase
    model_properties = ['ballots', 'department', 'description', 'name', 'phase_type', 'secret', 'status', 'target', 'title']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


class NewVotingPhaseCell(NewFormCell):

    def _prepare_form_for_render(self):
        departments = self._request.current_user.managed_departments
        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments)
        self._form.prepare_for_render(items)


class EditVotingPhaseCell(EditFormCell):

    def _prepare_form_for_render(self):
        self._form_data = self._model.to_dict()
        departments = self._request.current_user.managed_departments
        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments, self._model)
        self._form.prepare_for_render(items)
