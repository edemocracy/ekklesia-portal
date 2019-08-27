from morepath import redirect
#from webob.exc import HTTPBadRequest
from {{ cookiecutter.app_name }}.app import App
from {{ cookiecutter.app_name }}.database.datamodel import {{ cookiecutter.ConceptName }}
from {{ cookiecutter.app_name }}.identity_policy import NoIdentity
from {{ cookiecutter.app_name }}.permission import CreatePermission, EditPermission
from .{{ cookiecutter.concept_name }}_cells import {{ cookiecutter.ConceptName }}Cell, {{ cookiecutter.ConceptNames }}Cell, New{{ cookiecutter.ConceptName }}Cell, Edit{{ cookiecutter.ConceptName }}Cell
from .{{ cookiecutter.concept_name }}_contracts import {{ cookiecutter.ConceptName }}Form
#from .{{ cookiecutter.concept_name }}_helper import
from .{{ cookiecutter.concept_names }} import {{ cookiecutter.ConceptNames }}


@App.permission_rule(model={{ cookiecutter.ConceptNames }}, permission=CreatePermission)
def {{ cookiecutter.concept_names }}_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model={{ cookiecutter.ConceptName }}, permission=EditPermission)
def {{ cookiecutter.concept_name }}_edit_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model={{ cookiecutter.ConceptNames }}, path='{{cookiecutter.concept_names}}')
def {{ cookiecutter.concept_names }}():
    return {{ cookiecutter.ConceptNames }}()


@App.path(model={{ cookiecutter.ConceptName }}, path='{{ cookiecutter.concept_names }}/{id}')
def {{ cookiecutter.concept_name }}(request, id):
    return request.q({{ cookiecutter.ConceptName }}).get(id)


@App.html(model={{ cookiecutter.ConceptNames }})
def index(self, request):
    cell = {{ cookiecutter.ConceptNames }}Cell(self, request, show_new_button=True)
    return cell.show()


@App.html(model={{ cookiecutter.ConceptNames }}, name='new', permission=CreatePermission)
def new(self, request):
    form = {{ cookiecutter.ConceptName }}Form(request, request.link(self))
    return New{{ cookiecutter.ConceptName }}Cell(request, form, form_data={}).show()


# this level of abstraction is nice, but the goal is:
# @App.html_create({{ cookiecutter.ConceptName }})
@App.html_form_post(model={{ cookiecutter.ConceptNames }}, form={{ cookiecutter.ConceptName }}Form, cell=New{{ cookiecutter.ConceptName }}Cell, permission=CreatePermission)
def create(self, request, appstruct):
    {{ cookiecutter.concept_name }} = {{ cookiecutter.ConceptName }}(**appstruct)
    request.db_session.add({{ cookiecutter.concept_name }})
    request.db_session.flush()
    return redirect(request.link({{ cookiecutter.concept_name }}))


@App.html(model={{ cookiecutter.ConceptName }})
def show(self, request):
    cell = {{ cookiecutter.ConceptName }}Cell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model={{ cookiecutter.ConceptName }}, name='edit', permission=EditPermission)
def edit(self, request):
    form = {{ cookiecutter.ConceptName }}Form(request, request.link(self))
    return Edit{{ cookiecutter.ConceptName }}Cell(self, request, form).show()


# this level of abstraction is nice, but the goal is:
# @App.html_update({{ cookiecutter.ConceptName }})
@App.html_form_post(model={{ cookiecutter.ConceptName }}, form={{ cookiecutter.ConceptName }}Form, cell=Edit{{ cookiecutter.ConceptName }}Cell, permission=EditPermission)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
