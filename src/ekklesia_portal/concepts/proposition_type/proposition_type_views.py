from morepath import redirect

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import PropositionType
from ekklesia_portal.permission import CreatePermission, EditPermission

from .proposition_type_cells import EditPropositionTypeCell, NewPropositionTypeCell, PropositionTypeCell, PropositionTypesCell
from .proposition_type_contracts import PropositionTypeForm
from .proposition_types import PropositionTypes


@App.permission_rule(model=PropositionTypes, permission=CreatePermission)
def proposition_types_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=PropositionType, permission=EditPermission)
def proposition_type_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=PropositionTypes, path='proposition_types')
def proposition_types():
    return PropositionTypes()


@App.html(model=PropositionTypes)
def index(self, request):
    cell = PropositionTypesCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=PropositionTypes, name='new', permission=CreatePermission)
def new(self, request):
    form = PropositionTypeForm(request, request.link(self))
    return NewPropositionTypeCell(request, form, form_data={}).show()


@App.html_form_post(
    model=PropositionTypes, form=PropositionTypeForm, cell=NewPropositionTypeCell, permission=CreatePermission
)
def create(self, request, appstruct):
    proposition_type = PropositionType(**appstruct)
    request.db_session.add(proposition_type)
    request.db_session.flush()
    return redirect(request.link(proposition_type))


@App.path(model=PropositionType, path='proposition_types/{id}')
def proposition_type(request, id):
    return request.q(PropositionType).get(id)


@App.html(model=PropositionType)
def show(self, request):
    cell = PropositionTypeCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=PropositionType, name='edit', permission=EditPermission)
def edit(self, request):
    form = PropositionTypeForm(request, request.link(self))
    return EditPropositionTypeCell(self, request, form).show()


@App.html_form_post(
    model=PropositionType, form=PropositionTypeForm, cell=EditPropositionTypeCell, permission=EditPermission
)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
