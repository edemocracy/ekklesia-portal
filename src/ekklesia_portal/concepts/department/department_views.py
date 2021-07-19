from morepath import redirect

# from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Department
from ekklesia_portal.lib.identity import identity_manages_department
from ekklesia_portal.permission import CreatePermission, EditPermission

from .department_cells import DepartmentCell, DepartmentsCell, EditDepartmentCell, NewDepartmentCell
from .department_contracts import DepartmentForm
# from .department_helper import
from .departments import Departments


@App.permission_rule(model=Departments, permission=CreatePermission)
def departments_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=Department, permission=EditPermission)
def department_edit_permission(identity, model, permission):
    return identity_manages_department(identity, model)


@App.path(model=Departments, path='departments')
def departments():
    return Departments()


@App.path(model=Department, path='departments/{id}')
def department(request, id):
    return request.q(Department).get(id)


@App.html(model=Departments)
def index(self, request):
    cell = DepartmentsCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Departments, name='new', permission=CreatePermission)
def new(self, request):
    form = DepartmentForm(request, request.link(self))
    return NewDepartmentCell(request, form, form_data={}).show()


# this level of abstraction is nice, but the goal is:
# @App.html_create(Department)
@App.html_form_post(model=Departments, form=DepartmentForm, cell=NewDepartmentCell, permission=CreatePermission)
def create(self, request, appstruct):
    department = Department(**appstruct)
    request.db_session.add(department)
    request.db_session.flush()
    return redirect(request.link(department))


@App.html(model=Department)
def show(self, request):
    cell = DepartmentCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=Department, name='edit', permission=EditPermission)
def edit(self, request):
    form = DepartmentForm(request, request.link(self))
    return EditDepartmentCell(self, request, form).show()


# this level of abstraction is nice, but the goal is:
# @App.html_update(Department)
@App.html_form_post(model=Department, form=DepartmentForm, cell=EditDepartmentCell, permission=EditPermission)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
