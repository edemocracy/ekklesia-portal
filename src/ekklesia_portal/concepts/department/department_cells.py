from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.database.datamodel import Department
from ekklesia_portal.permission import CreatePermission, EditPermission
from .departments import Departments


class DepartmentsCell(LayoutCell):
    model = Departments

    def departments(self):
        return list(self._model.departments(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


class DepartmentCell(LayoutCell):
    model = Department
    model_properties = ['areas', 'description', 'name', 'voting_phases']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


class NewDepartmentCell(NewFormCell):
    pass


class EditDepartmentCell(EditFormCell):
    pass