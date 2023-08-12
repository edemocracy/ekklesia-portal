from ekklesia_common.permission import CreatePermission
from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Ballot, SubjectArea, VotingPhase
from ekklesia_portal.enums import PropositionStatus, VotingStatus
from ekklesia_portal.lib.identity import identity_manages_department, identity_manages_any_department
from ekklesia_portal.permission import EditPermission

from .ballot_cells import BallotsCell, NewBallotCell, BallotCell, EditBallotCell
from .ballot_contracts import BallotForm
from .ballots import Ballots


@App.permission_rule(model=Ballots, permission=CreatePermission)
def ballots_create_permission(identity, model, permission):
    return identity_manages_any_department(identity)


@App.permission_rule(model=Ballot, permission=EditPermission)
def ballot_edit_permission(identity, model, permission):
    return identity_manages_department(identity, model.area.department)


@App.path(model=Ballots, path='b')
def ballots():
    return Ballots()


@App.path(model=Ballot, path='b/{id}')
def ballot(request, id):
    return request.q(Ballot).get(id)


@App.html(model=Ballots)
def index(self, request):
    cell = BallotsCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Ballots, name='new', permission=CreatePermission)
def new(self, request):
    form = BallotForm(request, request.link(self))
    return NewBallotCell(request, form, form_data={}).show()


@App.html_form_post(
    model=Ballots, form=BallotForm, cell=NewBallotCell, permission=CreatePermission
)
def create(self, request, appstruct):
    area = request.q(SubjectArea).get(appstruct['area_id']) if appstruct['area_id'] else None
    voting_phase = request.q(VotingPhase).get(appstruct['voting_id']) if appstruct['voting_id'] else None

    department_id = None

    if area and voting_phase:
        if area.department_id != voting_phase.department_id:
            return HTTPBadRequest("area doesn't belong to the same department as the voting phase")
        department_id = area.department_id
    elif area:
        department_id = area.department_id
    elif voting_phase:
        department_id = voting_phase.department_id

    if department_id and not request.identity.has_global_admin_permissions:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
        if not department_allowed:
            return HTTPBadRequest("department not allowed")

    ballot = Ballot(**appstruct)
    request.db_session.add(ballot)
    request.db_session.flush()
    return redirect(request.link(ballot))


@App.html(model=Ballot)
def show(self, request):
    cell = BallotCell(self, request, show_edit_button=True, show_details=True, show_propositions=True)
    return cell.show()


@App.html(model=Ballot, name='edit', permission=EditPermission)
def edit(self, request):
    form = BallotForm(request, request.link(self))
    return EditBallotCell(self, request, form).show()


@App.html_form_post(model=Ballot, form=BallotForm, cell=EditBallotCell, permission=EditPermission)
def update(self, request, appstruct):
    area = request.q(SubjectArea).get(appstruct['area_id']) if appstruct['area_id'] else None
    voting_phase = request.q(VotingPhase).get(appstruct['voting_id']) if appstruct['voting_id'] else None

    department_id = None

    if area and voting_phase:
        if area.department_id != voting_phase.department_id:
            return HTTPBadRequest("area doesn't belong to the same department as the voting phase")
        department_id = area.department_id
    elif area:
        department_id = area.department_id
    elif voting_phase:
        department_id = voting_phase.department_id

    if department_id and not request.identity.has_global_admin_permissions:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
        if not department_allowed:
            return HTTPBadRequest("department not allowed")

    # Move proposition states to scheduled when adding ballot to voting phase
    if voting_phase and voting_phase.status == VotingStatus.PREPARING:
        for proposition in self.propositions:
            if proposition.status == PropositionStatus.QUALIFIED:
                proposition.status = PropositionStatus.SCHEDULED

    self.update(**appstruct)
    return redirect(request.link(self))
