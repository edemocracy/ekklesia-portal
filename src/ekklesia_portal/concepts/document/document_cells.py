from markupsafe import Markup
from ekklesia_portal.app import App
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.concepts.proposition.propositions import Propositions
from ekklesia_portal.datamodel import Document, Department, PropositionType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .document_helper import items_for_document_select_widgets, markdown_with_propose_change
from .documents import Documents


@App.cell(Documents)
class DocumentsCell(LayoutCell):

    def documents(self):
        return list(self._model.documents(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(Document)
class DocumentCell(LayoutCell):

    model_properties = ['name', 'lang', 'text', 'description']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)

    def propose_change_url(self):
        return self.link(self._model, name='propose_change')

    def department_name(self):
        return self._model.area.department.name

    def subject_area_name(self):
        return self._model.area.name

    def proposition_type_name(self):
        return self._model.proposition_type.name


@App.cell(Document, 'propose_change')
class DocumentProposeChangeCell(LayoutCell):

    model_properties = ['name', 'lang', 'description']

    def text_with_propose_change(self):
        propose_change_url_template = self.link(Propositions(document=self._model.id, section='SECTION'),
                                                name='+new_draft')
        html = markdown_with_propose_change(propose_change_url_template, self._model.text)
        return Markup(html)

    def area_name(self):
        return self._model.area.name

    def department_name(self):
        return self._model.area.department.name

    def explanation(self):
        return customizable_text(self._request, 'document_propose_change_explanation')


@App.cell(Documents, 'new')
class NewDocumentCell(NewFormCell):

    def _prepare_form_for_render(self):
        identity = self._request.identity
        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        proposition_types = self._request.q(PropositionType)
        items = items_for_document_select_widgets(self._model, departments, proposition_types)
        self._form.prepare_for_render(items)


@App.cell(Document, 'edit')
class EditDocumentCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        identity = self._request.identity
        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        proposition_types = self._request.q(PropositionType)
        items = items_for_document_select_widgets(self._model, departments, proposition_types)
        self._form.prepare_for_render(items)
