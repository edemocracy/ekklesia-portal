from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import Department
from ekklesia_portal.permission import CreatePermission, EditPermission

from .departments import Departments


@App.cell()
class DepartmentsCell(LayoutCell):

    _model: Departments

    def departments(self):
        return list(self._model.departments(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button'
                                ) and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell()
class DepartmentCell(LayoutCell):

    _model: Department
    model_properties = ['areas', 'description', 'name', 'voting_phases']

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)

    def num_members(self):
        return len(self._model.members)


@App.cell()
class NewDepartmentCell(NewFormCell):

    _model: Departments


@App.cell()
class EditDepartmentCell(EditFormCell):

    _model: Department
