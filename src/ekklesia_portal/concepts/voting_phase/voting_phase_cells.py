from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.database.datamodel import VotingPhase, VotingPhaseType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phases import VotingPhases
from .voting_phase_helper import items_for_voting_phase_select_widgets


@App.cell(VotingPhases)
class VotingPhasesCell(LayoutCell):

    def voting_phases(self):
        return list(self._model.voting_phases(self._request.q))

    def show_new_button(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(VotingPhase)
class VotingPhaseCell(LayoutCell):
    model_properties = ['ballots', 'department', 'description', 'name', 'phase_type', 'secret', 'status', 'target', 'title']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)

    def propositions(self):
        return [p for b in self._model.ballots for p in b.propositions]


@App.cell(VotingPhases, 'new')
class NewVotingPhaseCell(NewFormCell):

    def _prepare_form_for_render(self):
        departments = self._request.current_user.managed_departments
        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments)
        self._form.prepare_for_render(items)


@App.cell(VotingPhase, 'edit')
class EditVotingPhaseCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        departments = self._request.current_user.managed_departments
        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments, self._model)
        self._form.prepare_for_render(items)
