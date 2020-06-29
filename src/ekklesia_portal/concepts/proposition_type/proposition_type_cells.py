from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.datamodel import Policy, PropositionType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .proposition_type_helper import items_for_proposition_type_select_widgets
from .proposition_types import PropositionTypes


@App.cell(PropositionTypes)
class PropositionTypesCell(LayoutCell):

    def proposition_types(self):
        return list(self._model.proposition_types(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(PropositionType)
class PropositionTypeCell(LayoutCell):
    model_properties = ['name', 'description', 'policy']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


@App.cell(PropositionTypes, 'new')
class NewPropositionTypeCell(NewFormCell):

    def _prepare_form_for_render(self):
        policies = self._request.q(Policy)
        items = items_for_proposition_type_select_widgets(policies)
        self._form.prepare_for_render(items)


@App.cell(PropositionType, 'edit')
class EditPropositionTypeCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        policies = self._request.q(Policy)
        items = items_for_proposition_type_select_widgets(policies)
        self._form.prepare_for_render(items)
