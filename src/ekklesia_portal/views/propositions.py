from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS
from ekklesia_portal.database.datamodel import Proposition, Tag
from ekklesia_portal.cells.proposition import PropositionCell, PropositionsCell, NewPropositionCell
from ekklesia_portal.collections.propositions import Propositions


@App.path(model=Propositions, path='propositions')
def propositions(request, searchterm=None, tag=None, mode="sorted"):
    return Propositions(mode, searchterm, tag)


@App.path(model=Proposition, path="/propositions/{proposition_id}", variables=lambda o: dict(proposition_id=o.id))
def proposition(request, proposition_id):
    proposition = request.q(Proposition).get(proposition_id)
    return proposition


@App.html(model=Proposition)
def show(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='discussion')
    return cell.show()


@App.html(model=Proposition, name='associated')
def show_associated(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='associated')
    return cell.show()


@App.html(model=Propositions)
def index(self, request):
    return PropositionsCell(self, request).show()


@App.html(model=Propositions, name='new')
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


@App.html(model=Propositions, request_method='POST')
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
