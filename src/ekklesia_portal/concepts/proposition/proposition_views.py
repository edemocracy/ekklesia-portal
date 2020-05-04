import case_conversion
from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Ballot, Proposition, SubjectArea, Supporter
from ekklesia_portal.enums import PropositionStatus
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS
from ekklesia_portal.permission import CreatePermission, EditPermission, SupportPermission

from .proposition_cells import NewPropositionCell, EditPropositionCell, PropositionCell, PropositionsCell
from .proposition_contracts import PropositionNewForm, PropositionEditForm
from .propositions import Propositions
from .proposition_helper import get_or_create_tags


@App.permission_rule(model=Propositions, permission=CreatePermission)
def propositions_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=Proposition, permission=SupportPermission)
def proposition_support_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=Proposition, permission=EditPermission)
def proposition_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


App.path(path='p')(Propositions)


@App.path(model=Proposition, path="/p/{id}/{slug}", variables=lambda o: dict(id=o.id, slug=case_conversion.dashcase(o.title)))
def proposition(request, id, slug):
    proposition = request.q(Proposition).get(id)
    if case_conversion.dashcase(proposition.title) == slug:
        return proposition
    else:
        return redirect("/p/"+id+"/"+case_conversion.dashcase(proposition.title))


@App.path(path='/p/{id}')
class PropositionRedirect:
    def __init__(self, id):
        self.id = id


@App.html(model=Proposition)
def show(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, show_edit_button=True, active_tab='discussion')
    return cell.show()


@App.html(model=Proposition, name='associated')
def associated(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='associated')
    return cell.show()


@App.html(model=Proposition, request_method='POST', name='support', permission=SupportPermission)
def support(self, request):
    if 'support' not in request.POST and 'retract' not in request.POST:
        raise HTTPBadRequest()

    user_id = request.current_user.id
    supporter = request.db_session.query(Supporter).filter_by(member_id=user_id, proposition_id=self.id).scalar()
    if 'support' in request.POST:
        if supporter is None:
            supporter = Supporter(member_id=user_id, proposition_id=self.id)
            request.db_session.add(supporter)
        elif supporter.status in ('retracted', 'expired'):
            supporter.status = 'active'
    elif 'retract' in request.POST and supporter is not None and supporter.status != 'retracted':
        supporter.status = 'retracted'

    return redirect(request.link(self))


@App.html(model=Propositions)
def index(self, request):
    return PropositionsCell(self, request).show()


@App.html(model=Propositions, name='new', permission=CreatePermission)
def new(self, request):
    from_data = request.GET.get("from_data")
    source = request.GET.get("source")

    if from_data and source:
        # pre-fill new proposition form from a URL returning data formatted as `from_format`
        # 'for supported formats, see 'PROPOSITION_IMPORT_HANDLERS'
        importer_config = getattr(request.app.settings.importer, source)

        if importer_config is None:
            raise ValueError("unsupported proposition source: " + source)

        import_schema = importer_config['schema']
        import_handler = PROPOSITION_IMPORT_HANDLERS.get(import_schema)
        if import_handler is None:
            raise ValueError("unsupported proposition import schema: " + import_schema)

        form_data = import_handler(importer_config['base_url'], from_data)
    else:
        form_data = {}

    form = PropositionNewForm(request, request.class_link(Propositions))
    return NewPropositionCell(request, form, form_data).show()


@App.html_form_post(model=Propositions, form=PropositionNewForm, cell=NewPropositionCell, permission=CreatePermission)
def create(self, request, appstruct):
    appstruct['tags'] = get_or_create_tags(request.db_session, appstruct['tags'])
    relation_type = appstruct.pop('relation_type')
    related_proposition_id = appstruct.pop('related_proposition_id')
    if relation_type and related_proposition_id:
        related_proposition = request.db_session.query(Proposition).get(related_proposition_id)
        if related_proposition is None:
            raise HTTPBadRequest()

        # modifiying and replacing propositions are put in the existing ballot of the related proposition
        ballot = related_proposition.ballot

        if relation_type == 'modifies':
            appstruct['modifies'] = related_proposition
        elif relation_type == 'replaces':
            appstruct['replaces'] = related_proposition
    else:
        # create a new ballot as "container" for the proposition
        area = request.q(SubjectArea).get(appstruct['area_id']) if appstruct['area_id'] else None

        if area is None or area.department not in request.current_user.departments:
            return HTTPBadRequest()

        ballot = Ballot(area=area)

    del appstruct['area_id']

    proposition = Proposition(ballot=ballot, **appstruct)
    request.db_session.add(proposition)
    request.db_session.flush()

    return redirect(request.link(proposition))


@App.view(model=PropositionRedirect)
def proposition_redirect(self, request):
    proposition = request.q(Proposition).get(self.id)
    return redirect(request.link(proposition))


@App.html(model=Proposition, name='edit', permission=EditPermission)
def edit(self, request):
    form = PropositionEditForm(request, request.link(self))
    return EditPropositionCell(self, request, form).show()


@App.html_form_post(model=Proposition, form=PropositionEditForm, cell=EditPropositionCell, permission=EditPermission)
def update(self, request, appstruct):
    appstruct['tags'] = get_or_create_tags(request.db_session, appstruct['tags'])
    self.update(**appstruct)
    return redirect(request.link(self))
