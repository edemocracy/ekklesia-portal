from morepath import redirect

# from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Policy
from ekklesia_portal.permission import CreatePermission, EditPermission

# from .policy_helper import
from .policies import Policies
from .policy_cells import EditPolicyCell, NewPolicyCell, PoliciesCell, PolicyCell
from .policy_contracts import PolicyForm


@App.permission_rule(model=Policies, permission=CreatePermission)
def policies_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=Policy, permission=EditPermission)
def policy_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=Policies, path='policies')
def policies():
    return Policies()


@App.path(model=Policy, path='policies/{id}')
def policy(request, id):
    return request.q(Policy).get(id)


@App.html(model=Policies)
def index(self, request):
    cell = PoliciesCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Policies, name='new', permission=CreatePermission)
def new(self, request):
    form = PolicyForm(request, request.link(self))
    return NewPolicyCell(request, form, form_data={}).show()


@App.html_form_post(model=Policies, form=PolicyForm, cell=NewPolicyCell, permission=CreatePermission)
def create(self, request, appstruct):
    policy = Policy(**appstruct)
    request.db_session.add(policy)
    request.db_session.flush()
    return redirect(request.link(policy))


@App.html(model=Policy)
def show(self, request):
    cell = PolicyCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=Policy, name='edit', permission=EditPermission)
def edit(self, request):
    form = PolicyForm(request, request.link(self))
    return EditPolicyCell(self, request, form).show()


@App.html_form_post(model=Policy, form=PolicyForm, cell=EditPolicyCell, permission=EditPermission)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
