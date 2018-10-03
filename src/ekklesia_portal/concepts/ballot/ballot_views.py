from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Ballot, SubjectArea, VotingPhase
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.permission import EditPermission
from .ballot_cells import BallotCell, BallotsCell, EditBallotCell
from .ballots import Ballots
from .ballot_contracts import BallotForm
from .ballot_helper import items_for_ballot_select_widgets


@App.permission_rule(model=Ballot, permission=EditPermission)
def ballot_edit_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model=Ballots, path='b')
def ballots():
    return Ballots()


@App.html(model=Ballots)
def index(self, request):
    cell = BallotsCell(self, request)
    return cell.show()


@App.path(model=Ballot, path='b/{id}')
def ballot(request, id):
    return request.q(Ballot).get(id)


@App.html(model=Ballot, name='edit', permission=EditPermission)
def edit(self, request):
    form_data = self.to_dict()
    items = items_for_ballot_select_widgets(self, departments=request.current_user.managed_departments)
    form = BallotForm(request, request.link(self), items)
    return EditBallotCell(form, request, form_data).show()


@App.html(model=Ballot, request_method='POST', permission=EditPermission)
def update(self, request):
    controls = request.POST.items()
    form = BallotForm(request)
    try:
        appstruct = form.validate(controls)
    except ValidationFailure:
        items = items_for_ballot_select_widgets(self, departments=request.current_user.managed_departments)
        form = BallotForm(request, request.link(self), items)
        return EditBallotCell(form, request, None).show()

    area = request.q(SubjectArea).get(appstruct['area_id']) if appstruct['area_id'] else None
    voting_phase = request.q(VotingPhase).get(appstruct['voting_id']) if appstruct['voting_id'] else None

    department_id = None

    if area and voting_phase:
        if area.department_id != voting_phase.department_id:
            return HTTPBadRequest()
        department_id = area.department_id
    elif area:
        department_id = area.department_id
    elif voting_phase:
        department_id = voting_phase.department_id

    if department_id:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
        if not department_allowed:
            return HTTPBadRequest()

    self.update(**appstruct)
    return redirect(request.link(self))


@App.html(model=Ballot)
def show(self, request):
    cell = BallotCell(self, request, show_edit_button=True, show_propositions=True)
    return cell.show()
