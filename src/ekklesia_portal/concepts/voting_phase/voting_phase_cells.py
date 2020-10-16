from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import Department, VotingPhase, VotingPhaseType
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.permission import CreatePermission, EditPermission

from .voting_phase_helper import items_for_voting_phase_select_widgets
from .voting_phase_permissions import ManageVotingPermission
from .voting_phases import VotingPhases


@App.cell(VotingPhases)
class VotingPhasesCell(LayoutCell):

    def voting_phases(self):
        return list(self._model.voting_phases(self._request.q))

    def show_new_button(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(VotingPhase)
class VotingPhaseCell(LayoutCell):
    model_properties = [
        'ballots', 'department', 'description', 'name', 'phase_type', 'secret', 'status', 'target', 'title'
    ]

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)

    def propositions(self):
        return [p for b in self._model.ballots for p in b.propositions]


@App.cell(VotingPhases, 'new')
class NewVotingPhaseCell(NewFormCell):

    def _prepare_form_for_render(self):
        identity = self._request.identity

        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments)
        self._form.prepare_for_render(items)


@App.cell(VotingPhase, 'edit')
class EditVotingPhaseCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        identity = self._request.identity

        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        phase_types = self._request.q(VotingPhaseType)
        items = items_for_voting_phase_select_widgets(phase_types, departments, self._model)
        self._form.prepare_for_render(items)

    def show_create_voting(self):
        return self._model.status == VotingStatus.SCHEDULED and self._request.permitted_for_current_user(self._model, ManageVotingPermission)

    def voting_modules(self):
        # value is True if there's already a configured voting
        return [(name, name not in self._model.voting_module_data) for name in self._model.department.voting_module_settings]

    def create_voting_action(self):
        return self._request.link(self._model, "create_voting")
