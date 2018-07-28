from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS
from ekklesia_portal.database.datamodel import Proposition, Tag, Supporter
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.permission import CreatePermission, SupportPermission
from .proposition_cells import PropositionCell, PropositionsCell, NewPropositionCell
from .propositions import Propositions


@App.permission_rule(model=Propositions, permission=CreatePermission)
def propositions_create_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=Proposition, permission=SupportPermission)
def proposition_support_permission(identity, model, permission):
    return identity != NoIdentity


@App.path(model=Propositions, path='propositions')
def propositions(request, search=None, tag=None, mode="sorted"):
    return Propositions(mode, search, tag)


@App.path(model=Proposition, path="/propositions/{proposition_id}", variables=lambda o: dict(proposition_id=o.id))
def proposition(request, proposition_id):
    proposition = request.q(Proposition).get(proposition_id)
    return proposition


@App.html(model=Proposition)
def show(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='discussion')
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

    return NewPropositionCell(self.form(request.class_link(Propositions)), request, form_data).show()


@App.html(model=Propositions, request_method='POST', permission=CreatePermission)
def create(self, request):
    controls = request.POST.items()
    form = self.form(request.class_link(Propositions))
    try:
        appstruct = form.validate(controls)
    except ValidationFailure as e:
        return NewPropositionCell(form, request, None).show()

    tag_names = appstruct['tags']

    if tag_names:
        tags = request.db_session.query(Tag).filter(Tag.name.in_(tag_names)).all()

        new_tag_names = set(tag_names) - {t.name for t in tags}

        for tag_name in new_tag_names:
            tag = Tag(name=tag_name)
            tags.append(tag)

        appstruct['tags'] = tags

    relation_type = appstruct.pop('relation_type')
    related_proposition_id = appstruct.pop('related_proposition_id')
    if relation_type and related_proposition_id:
        related_proposition = request.db_session.query(Proposition).get(related_proposition_id)
        if related_proposition is None:
            raise HTTPBadRequest()

        if relation_type == 'modifies':
            appstruct['modifies'] = related_proposition
        elif relation_type == 'replaces':
            appstruct['replaces'] = related_proposition

    proposition = Proposition(**appstruct)
    request.db_session.add(proposition)
    request.db_session.flush()

    return redirect(request.link(proposition))
