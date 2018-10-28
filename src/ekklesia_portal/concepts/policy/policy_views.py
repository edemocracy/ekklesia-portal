from datetime import timedelta
from deform import ValidationFailure
from morepath import redirect
#from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Policy
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.permission import CreatePermission, EditPermission
from .policy_cells import PolicyCell, PoliciesCell, NewPolicyCell, EditPolicyCell
from .policy_contracts import PolicyForm
#from .policy_helper import
from .policies import Policies


@App.permission_rule(model=Policies, permission=CreatePermission)
def policies_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=Policy, permission=EditPermission)
def policy_edit_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model=Policies, path='policies')
def policies():
    return Policies()


@App.html(model=Policies)
def index(self, request):
    cell = PoliciesCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Policies, name='new', permission=CreatePermission)
def new(self, request):
    form = PolicyForm(request, request.link(self))
    return NewPolicyCell(request, form, form_data={}).show()


@App.html(model=Policies, request_method='POST', permission=CreatePermission)
def create(self, request):
    controls = request.POST.items()
    form = PolicyForm(request, request.link(self))
    try:
        appstruct = form.validate(controls)
    except ValidationFailure:
        return NewPolicyCell(request, form).show()

    policy = Policy(**appstruct)
    request.db_session.add(policy)
    request.db_session.flush()

    return redirect(request.link(policy))


@App.path(model=Policy, path='policies/{id}')
def policy(request, id):
    return request.q(Policy).get(id)


@App.html(model=Policy)
def show(self, request):
    cell = PolicyCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=Policy, name='edit', permission=EditPermission)
def edit(self, request):
    form = PolicyForm(request, request.link(self))
    return EditPolicyCell(self, request, form).show()


@App.html(model=Policy, request_method='POST', permission=EditPermission)
def update(self, request):
    controls = request.POST.items()
    form = PolicyForm(request, request.link(self))
    try:
        appstruct = form.validate(controls)
    except ValidationFailure:
        return EditPolicyCell(self, request, form).show()

    self.update(**appstruct)
    return redirect(request.link(self))
