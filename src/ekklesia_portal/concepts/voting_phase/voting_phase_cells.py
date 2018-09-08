from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import FormCell
from ekklesia_portal.database.datamodel import VotingPhase
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phases import VotingPhases


class VotingPhasesCell(LayoutCell):
    model = VotingPhases

    def voting_phases(self):
        return list(self._model.voting_phases(self._request.q))

    def show_new_button(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)


class VotingPhaseCell(LayoutCell):
    model = VotingPhase
    model_properties = ['ballots', 'department', 'description', 'name', 'phase_type', 'secret', 'target', 'title']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


class NewVotingPhaseCell(FormCell):
    pass


class EditVotingPhaseCell(FormCell):
    pass
