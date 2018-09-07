from deform import ValidationFailure
from morepath import redirect
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import VotingPhase
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.permission import CreatePermission, EditPermission
from .voting_phase_cells import VotingPhaseCell, VotingPhasesCell, NewVotingPhaseCell, EditVotingPhaseCell
from .voting_phases import VotingPhases
from .voting_phase_contracts import VotingPhaseForm


@App.permission_rule(model=VotingPhases, permission=CreatePermission)
def voting_phases_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=VotingPhase, permission=EditPermission)
def voting_phase_edit_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model=VotingPhases, path='v')
def voting_phases():
    return VotingPhases()


@App.html(model=VotingPhases)
def index(self, request):
    cell = VotingPhasesCell(self, request)
    return cell.show()


@App.html(model=VotingPhases, name='new', permission=CreatePermission)
def new(self, request):
    form_data = {}
    return NewVotingPhaseCell(self.form(request.class_link(VotingPhases), request), request, form_data).show()


@App.html(model=VotingPhases, request_method='POST', permission=CreatePermission)
def create(self, request):
    controls = request.POST.items()
    form = self.form(request.class_link(VotingPhases), request)
    try:
        appstruct = form.validate(controls)
    except ValidationFailure:
        return NewVotingPhaseCell(form, request, None).show()

    voting_phase = VotingPhase(**appstruct)
    request.db_session.add(voting_phase)
    request.db_session.flush()

    return redirect(request.link(voting_phase))


@App.path(model=VotingPhase, path='v/{id}/{slug}',  variables=lambda o: dict(id=o.id, slug=o.name or o.target or o.id))
def voting_phase(request, id, slug):
    return request.q(VotingPhase).get(id)


@App.html(model=VotingPhase, name='edit', permission=EditPermission)
def edit(self, request):
    form_data = self.to_dict()
    form = VotingPhaseForm(request, request.link(self))
    return EditVotingPhaseCell(form, request, form_data).show()


@App.html(model=VotingPhase, request_method='POST', permission=EditPermission)
def update(self, request):
    controls = request.POST.items()
    form = VotingPhaseForm(request, request.link(self))
    try:
        appstruct = form.validate(controls)
    except ValidationFailure:
        return EditVotingPhaseCell(form, request, None).show()

    self.update(**appstruct)
    return redirect(request.link(self))


@App.html(model=VotingPhase)
def show(self, request):
    cell = VotingPhaseCell(self, request, show_edit_button=True)
    return cell.show()
