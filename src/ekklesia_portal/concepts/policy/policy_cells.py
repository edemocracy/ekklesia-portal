from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.database.datamodel import Policy
from ekklesia_portal.permission import CreatePermission, EditPermission
from .policy_helper import items_for_policy_select_widgets
from .policies import Policies


class PoliciesCell(LayoutCell):
    model = Policies

    def policies(self):
        return list(self._model.policies(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


class PolicyCell(LayoutCell):
    model = Policy
    model_properties = ['name', 'majority', 'proposition_expiration', 'qualification_minimum', 'qualification_quorum', 'range_max',
                        'range_small_max', 'range_small_options', 'secret_minimum', 'secret_quorum', 'submitter_minimum',
                        'voting_duration', 'voting_system']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


class NewPolicyCell(NewFormCell):

    def _prepare_form_for_render(self):
        items = items_for_policy_select_widgets()
        self._form.prepare_for_render(items)


class EditPolicyCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        items = items_for_policy_select_widgets()
        self._form.prepare_for_render(items)
