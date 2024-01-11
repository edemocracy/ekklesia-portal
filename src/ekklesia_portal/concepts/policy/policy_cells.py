from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import Policy
from ekklesia_portal.permission import CreatePermission, EditPermission

from .policies import Policies
from .policy_helper import items_for_policy_select_widgets


@App.cell()
class PoliciesCell(LayoutCell):

    _model: Policies

    def policies(self):
        return list(self._model.policies(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button'
                                ) and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell()
class PolicyCell(LayoutCell):

    _model: Policy
    model_properties = [
        'name', 'majority', 'proposition_expiration', 'qualification_minimum', 'qualification_quorum', 'range_max',
        'range_small_max', 'range_small_options', 'secret_minimum', 'secret_quorum', 'submitter_minimum',
        'voting_duration', 'voting_system'
    ]

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)


@App.cell()
class NewPolicyCell(NewFormCell):

    _model: Policies

    def _prepare_form_for_render(self):
        items = items_for_policy_select_widgets()
        self._form.prepare_for_render(items)


@App.cell()
class EditPolicyCell(EditFormCell):

    _model: Policy

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        items = items_for_policy_select_widgets()
        self._form.prepare_for_render(items)
