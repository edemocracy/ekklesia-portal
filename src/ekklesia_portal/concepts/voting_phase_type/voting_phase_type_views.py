from morepath import redirect
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import VotingPhaseType
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phase_type_cells import VotingPhaseTypeCell, VotingPhaseTypesCell, NewVotingPhaseTypeCell, EditVotingPhaseTypeCell
from .voting_phase_type_contracts import VotingPhaseTypeForm
from .voting_phase_types import VotingPhaseTypes


@App.permission_rule(model=VotingPhaseTypes, permission=CreatePermission)
def voting_phase_types_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=VotingPhaseType, permission=EditPermission)
def voting_phase_type_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=VotingPhaseTypes, path='voting_phase_types')
def voting_phase_types():
    return VotingPhaseTypes()


@App.path(model=VotingPhaseType, path='voting_phase_types/{id}')
def voting_phase_type(request, id):
    return request.q(VotingPhaseType).get(id)


@App.html(model=VotingPhaseTypes)
def index(self, request):
    cell = VotingPhaseTypesCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=VotingPhaseTypes, name='new', permission=CreatePermission)
def new(self, request):
    form = VotingPhaseTypeForm(request, request.link(self))
    return NewVotingPhaseTypeCell(request, form, form_data={}).show()


@App.html_form_post(
    model=VotingPhaseTypes, form=VotingPhaseTypeForm, cell=NewVotingPhaseTypeCell, permission=CreatePermission
)
def create(self, request, appstruct):
    voting_phase_type = VotingPhaseType(**appstruct)
    request.db_session.add(voting_phase_type)
    request.db_session.flush()
    return redirect(request.link(voting_phase_type))


@App.html(model=VotingPhaseType)
def show(self, request):
    cell = VotingPhaseTypeCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=VotingPhaseType, name='edit', permission=EditPermission)
def edit(self, request):
    form = VotingPhaseTypeForm(request, request.link(self))
    return EditVotingPhaseTypeCell(self, request, form).show()


@App.html_form_post(
    model=VotingPhaseType, form=VotingPhaseTypeForm, cell=EditVotingPhaseTypeCell, permission=EditPermission
)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
