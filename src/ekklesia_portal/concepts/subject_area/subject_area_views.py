from morepath import redirect
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import SubjectArea
from ekklesia_portal.permission import CreatePermission, EditPermission
from .subject_area_cells import SubjectAreaCell, SubjectAreasCell, NewSubjectAreaCell, EditSubjectAreaCell
from .subject_area_contracts import SubjectAreaForm
from .subject_areas import SubjectAreas


@App.permission_rule(model=SubjectAreas, permission=CreatePermission)
def subject_areas_create_permission(identity, model, permission):
    if identity.has_global_admin_permissions:
        return True

    return identity.user.managed_departments


@App.permission_rule(model=SubjectArea, permission=EditPermission)
def subject_area_edit_permission(identity, model, permission):
    if identity.has_global_admin_permissions:
        return True

    return model.department in identity.user.managed_departments


@App.path(model=SubjectAreas, path='subject_areas')
def subject_areas():
    return SubjectAreas()


@App.path(model=SubjectArea, path='subject_areas/{id}')
def subject_area(request, id):
    return request.q(SubjectArea).get(id)


@App.html(model=SubjectAreas)
def index(self, request):
    cell = SubjectAreasCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=SubjectAreas, name='new', permission=CreatePermission)
def new(self, request):
    form = SubjectAreaForm(request, request.link(self))
    return NewSubjectAreaCell(request, form, form_data={}).show()


@App.html_form_post(model=SubjectAreas, form=SubjectAreaForm, cell=NewSubjectAreaCell, permission=CreatePermission)
def create(self, request, appstruct):
    subject_area = SubjectArea(**appstruct)
    request.db_session.add(subject_area)
    request.db_session.flush()
    return redirect(request.link(subject_area))


@App.html(model=SubjectArea)
def show(self, request):
    cell = SubjectAreaCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=SubjectArea, name='edit', permission=EditPermission)
def edit(self, request):
    form = SubjectAreaForm(request, request.link(self))
    return EditSubjectAreaCell(self, request, form).show()


@App.html_form_post(model=SubjectArea, form=SubjectAreaForm, cell=EditSubjectAreaCell, permission=EditPermission)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
