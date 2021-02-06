from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Ballot, SubjectArea, VotingPhase, VotingIdCounter
from ekklesia_portal.permission import EditPermission
import logging

from .ballot_cells import BallotCell, BallotsCell, EditBallotCell
from .ballot_contracts import BallotForm
from .ballots import Ballots


@App.permission_rule(model=Ballot, permission=EditPermission)
def ballot_edit_permission(identity, model, permission):
    if identity.has_global_admin_permissions:
        return True

    return model.area.department in identity.user.managed_departments


@App.path(model=Ballots, path='b')
def ballots():
    return Ballots()


@App.path(model=Ballot, path='b/{id}')
def ballot(request, id):
    return request.q(Ballot).get(id)


@App.html(model=Ballots)
def index(self, request):
    cell = BallotsCell(self, request)
    return cell.show()


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
            return HTTPBadRequest()
        department_id = area.department_id
    elif area:
        department_id = area.department_id
    elif voting_phase:
        department_id = voting_phase.department_id

    if department_id and not request.identity.has_global_admin_permissions:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]
        if not department_allowed:
            return HTTPBadRequest()

    self.update(**appstruct)

    if self.voting_id is not None: 
        for proposition in self.propositions:
            if not proposition.voting_identifier and self.proposition_type.voting_identifier_template:
                v_id_cnt = request.q(VotingIdCounter).filter(VotingIdCounter.proposition_type_id == self.proposition_type_id, VotingIdCounter.voting_phase_id == self.voting_id).scalar()
                if v_id_cnt is None:
                    v_id_cnt = VotingIdCounter(proposition_type_id = self.proposition_type_id, voting_phase_id = self.voting_id, counter= 0)
                    request.db_session.add(v_id_cnt)
                v_id_cnt.counter += 1
                try:
                    proposition.voting_identifier= self.proposition_type.voting_identifier_template.format(v_id_cnt.counter)
                except Exception as e:
                    logging.error("proposition type {0}: invalid voting identifier template {1}".format(self.proposition_type.name, self.proposition_type.voting_identifier_template))

    return redirect(request.link(self))
