from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import FormCell
import ekklesia_portal.concepts.voting_phase.voting_phase_helper as voting_phase_helper
from ekklesia_portal.database.datamodel import Ballot
from ekklesia_portal.permission import CreatePermission, EditPermission
from .ballots import Ballots


class BallotsCell(LayoutCell):
    model = Ballots

    def ballots(self):
        return list(self._model.ballots(self._request.q))


class BallotCell(LayoutCell):
    model = Ballot
    model_properties = ['area', 'election', 'id', 'name', 'propositions', 'result', 'status', 'voting']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)

    def voting_phase_title(self):
        return voting_phase_helper.voting_phase_title(self._model.voting)


class EditBallotCell(FormCell):
    pass
