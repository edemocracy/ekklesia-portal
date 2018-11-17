from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import VotingPhase, Department, VotingPhaseType
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phase_cells import VotingPhaseCell, VotingPhasesCell, NewVotingPhaseCell, EditVotingPhaseCell
from .voting_phases import VotingPhases
from .voting_phase_contracts import VotingPhaseForm
from .voting_phase_helper import items_for_voting_phase_select_widgets


@App.permission_rule(model=VotingPhases, permission=CreatePermission)
def voting_phases_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=VotingPhase, permission=EditPermission)
def voting_phase_edit_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model=VotingPhases, path='v')
def voting_phases():
    return VotingPhases()


@App.path(model=VotingPhase, path='v/{id}/{slug}',  variables=lambda o: dict(id=o.id, slug=o.name or o.target or o.id))
def voting_phase(request, id, slug):
    return request.q(VotingPhase).get(id)


@App.html(model=VotingPhases)
def index(self, request):
    cell = VotingPhasesCell(self, request)
    return cell.show()


@App.html(model=VotingPhases, name='new', permission=CreatePermission)
def new(self, request):
    form = VotingPhaseForm(request, request.link(self))
    return NewVotingPhaseCell(request, form, form_data={}).show()


@App.html_form_post(model=VotingPhases, form=VotingPhaseForm, cell=NewVotingPhaseCell, permission=CreatePermission)
def create(self, request, appstruct):
    department_id = appstruct['department_id']
    department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
    voting_phase_type = request.q(VotingPhaseType).get(appstruct['phase_type_id'])

    if not department_allowed or voting_phase_type is None:
        return HTTPBadRequest()

    voting_phase = VotingPhase(**appstruct)
    request.db_session.add(voting_phase)
    request.db_session.flush()

    return redirect(request.link(voting_phase))


@App.html(model=VotingPhase, name='edit', permission=EditPermission)
def edit(self, request):
    form = VotingPhaseForm(request, request.link(self))
    return EditVotingPhaseCell(self, request, form).show()


@App.html_form_post(model=VotingPhase, form=VotingPhaseForm, cell=EditVotingPhaseCell, permission=EditPermission)
def update(self, request, appstruct):
    department_id = appstruct['department_id']
    department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
    voting_phase_type = request.q(VotingPhaseType).get(appstruct['phase_type_id'])

    if not department_allowed or voting_phase_type is None:
        return HTTPBadRequest()

    # after setting a target date, the state of the voting phase transitions to SCHEDULED
    if appstruct['target'] and self.target is None:
        appstruct['status'] = VotingStatus.SCHEDULED

    self.update(**appstruct)
    return redirect(request.link(self))


@App.html(model=VotingPhase)
def show(self, request):
    cell = VotingPhaseCell(self, request, show_edit_button=True)
    return cell.show()
