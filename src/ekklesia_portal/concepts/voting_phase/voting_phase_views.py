from ekklesia_common import md
from morepath import redirect
from webob.exc import HTTPBadRequest
from eliot import start_action

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import VotingPhase, VotingPhaseType
from ekklesia_portal.enums import VotingStatus, OpenSlidesVotingResult
from ekklesia_portal.lib.identity import identity_manages_department, identity_manages_any_department
from ekklesia_portal.lib.voting import InvalidVotingModule, prepare_module_config
from ekklesia_portal.permission import CreatePermission, EditPermission

from .voting_phase_cells import EditVotingPhaseCell, NewVotingPhaseCell, VotingPhaseCell, VotingPhasesCell
from .voting_phase_contracts import VotingPhaseForm
from .voting_phases import VotingPhases
from .voting_phase_permissions import ManageVotingPermission


@App.permission_rule(model=VotingPhases, permission=CreatePermission)
def voting_phases_create_permission(identity, model, permission):
    return identity_manages_any_department(identity)


@App.permission_rule(model=VotingPhase, permission=EditPermission)
def voting_phase_edit_permission(identity, model, permission):
    return identity_manages_department(identity, model.department)


@App.permission_rule(model=VotingPhase, permission=ManageVotingPermission)
def voting_phase_edit_permission(identity, model, permission):
    return identity_manages_department(identity, model.department)


@App.path(model=VotingPhases, path='v')
def voting_phases():
    return VotingPhases()


@App.path(model=VotingPhase, path='v/{id}/{slug}', variables=lambda o: dict(id=o.id, slug=o.name or o.target or o.id))
def voting_phase_path(request, id, slug):
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

    if not request.identity.has_global_admin_permissions:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]

        if not department_allowed:
            return HTTPBadRequest("department not allowed")

    voting_phase_type = request.q(VotingPhaseType).get(appstruct['phase_type_id'])

    if voting_phase_type is None:
        return HTTPBadRequest("voting phase type is missing")

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

    if not request.identity.has_global_admin_permissions:
        department_allowed = [d for d in request.current_user.managed_departments if d.id == department_id]

        if not department_allowed:
            return HTTPBadRequest("department not allowed")

    phase_type = request.q(VotingPhaseType).get(appstruct['phase_type_id'])

    if phase_type is None:
        return HTTPBadRequest("voting phase type is missing")

    previous_status = self.status

    self.update(**appstruct)

    # Fill values from voting phase type when transitioning from PREPARING to VOTING.
    # We don't want to touch these values anymore when VOTING even if the voting phase type changes
    if previous_status == VotingStatus.PREPARING and self.status == VotingStatus.VOTING:
        if not self.voting_days:
            self.voting_days = phase_type.voting_days
        if not self.registration_start_days:
            self.registration_start_days = phase_type.registration_start_days
        if not self.registration_end_days:
            self.registration_end_days = phase_type.registration_end_days

    return redirect(request.link(self))


@App.html(model=VotingPhase)
def show(self, request):
    cell = VotingPhaseCell(
        self, request, show_edit_button=True, show_voting_details=True, show_description=True, full_view=True
    )
    return cell.show()


@App.json(model=VotingPhase, name='spickerrr')
def spickerrr(self, request):
    propositions = [p for b in self.ballots for p in b.propositions]

    def serialize_proposition(proposition):
        proposition_type = proposition.ballot.proposition_type
        return {
            'url': request.link(proposition),
            'id': proposition.voting_identifier,
            'title': proposition.title,
            'type': proposition_type.name if proposition_type else None,
            'tags': ', '.join(t.name for t in proposition.tags),
            'text': md.convert(proposition.content),
            'remarks': md.convert(proposition.motivation)
        }

    return [serialize_proposition(p) for p in propositions]


@App.html(model=VotingPhase, name="create_voting", request_method="POST", permission=EditPermission)
def create_voting(self: VotingPhase, request):
    if not self.voting_can_be_created:
        raise HTTPBadRequest(f"Voting phase {self} is in the wrong state ({self.status}) or target date is not set ({self.target})")

    try:
        voting_module_name = request.POST["create_voting"]
    except KeyError:
        raise HTTPBadRequest("create_voting (voting module name) missing from POST data!")

    try:
        module_config = prepare_module_config(request.app, self.department, voting_module_name)
    except InvalidVotingModule as e:
        raise HTTPBadRequest(e.args[0])

    _create_voting = module_config["create_voting"]

    with start_action(action_type="create_voting", create_voting_func=_create_voting):
        self.voting_module_data[voting_module_name] = _create_voting(module_config, self)

    _ = request.i18n.gettext

    request.flash(_("voting_created_msg", voting_module=voting_module_name), "success")

    return redirect(request.link(self))


@App.html(model=VotingPhase, name="retrieve_voting", request_method="POST", permission=EditPermission)
def retrieve_voting(self, request):
    if not self.voting_can_be_retrieved:
        raise HTTPBadRequest(f"Voting phase {self} is in the wrong state ({self.status}) or target date is not set ({self.target})")

    try:
        voting_module_name = request.POST["retrieve_voting"]
    except KeyError:
        raise HTTPBadRequest("retrieve_voting (voting module name) missing from POST data!")

    voting_module_data = self.voting_module_data.get(voting_module_name)
    if not voting_module_data:
        raise HTTPBadRequest("Voting module is not configured")

    try:
        module_config = prepare_module_config(request.app, self.department, voting_module_name)
    except InvalidVotingModule as e:
        raise HTTPBadRequest(e.args[0])

    _retrieve_voting = module_config["retrieve_voting"]

    results = _retrieve_voting(module_config, voting_module_data)

    with start_action(action_type="apply_election_results") as action:
        result_objs = []
        for ballot in self.ballots:
            if str(ballot.id) in results:
                result = results.get(str(ballot.id))
                result_obj = {}
                for proposition in ballot.propositions:
                    if int(proposition.id) & ((2 ** 22) - 1) in result:
                        res = OpenSlidesVotingResult.ACCEPTED
                    else:
                        res = OpenSlidesVotingResult.REJECTED
                    result_obj[proposition.voting_identifier] = {"state": res}
                ballot.result = result_obj
                result_objs.append(result_obj)

        action.add_success_fields(results=result_objs)

    _ = request.i18n.gettext

    request.flash(_("voting_retrieved_msg", voting_module=voting_module_name), "success")

    return redirect(request.link(self))
