from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.datamodel import Department, SubjectArea
from ekklesia_portal.permission import CreatePermission, EditPermission
from .subject_area_helper import items_for_subject_area_select_widgets
from .subject_areas import SubjectAreas


@App.cell(SubjectAreas)
class SubjectAreasCell(LayoutCell):

    def subject_areas(self):
        return list(self._model.subject_areas(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(SubjectArea)
class SubjectAreaCell(LayoutCell):

    model_properties = ['description', 'name']

    def department_name(self):
        return self._model.department.name

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


@App.cell(SubjectAreas, 'new')
class NewSubjectAreaCell(NewFormCell):
    pass

    def _prepare_form_for_render(self):

        identity = self._request.identity
        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        items = items_for_subject_area_select_widgets(departments)
        self._form.prepare_for_render(items)


@App.cell(SubjectArea, 'edit')
class EditSubjectAreaCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)

        identity = self._request.identity
        if identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = identity.user.managed_departments

        items = items_for_subject_area_select_widgets(departments)
        self._form.prepare_for_render(items)
