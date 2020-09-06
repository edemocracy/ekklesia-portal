from re import L

import case_conversion
from ekklesia_common.lid import LID
from ekklesia_common.request import EkklesiaRequest as Request
from eliot import Message
from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text
from ekklesia_portal.concepts.document.document_helper import get_section_from_document
from ekklesia_portal.datamodel import Ballot, Changeset, Document, Proposition, PropositionType, SubjectArea, Supporter
from ekklesia_portal.enums import PropositionRelationType, PropositionStatus, PropositionVisibility
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS
from ekklesia_portal.lib.discourse import DiscourseConfig, DiscourseTopic, create_discourse_topic
from ekklesia_portal.permission import CreatePermission, EditPermission, SupportPermission, ViewPermission, WritePermission

from .proposition_cells import EditPropositionCell, NewPropositionCell, PropositionCell, PropositionNewDraftCell, PropositionsCell
from .proposition_contracts import PropositionEditForm, PropositionNewDraftForm, PropositionNewForm
from .proposition_helper import get_or_create_tags, proposition_slug
from .propositions import Propositions


@App.permission_rule(model=Proposition, permission=ViewPermission, identity=NoIdentity)
def proposition_view_permission_anon(identity, model, permission):
    if model.visibility == PropositionVisibility.PUBLIC:
        return True
    return False


@App.permission_rule(model=Proposition, permission=ViewPermission)
def proposition_view_permission(identity, model, permission):
    if model.visibility in (PropositionVisibility.PUBLIC, PropositionVisibility.UNLISTED):
        return True

    if model.submitted_by_user(identity.user):
        return True

    if model.ballot.area.department in identity.user.managed_departments:
        return True

    return identity.has_global_admin_permissions


@App.permission_rule(model=Propositions, permission=CreatePermission)
def propositions_create_permission(identity, model, permission):
    # TODO: All users can create propositions at the moment.
    # This must be limited to the users of a department (at least).
    return True


@App.permission_rule(model=Proposition, permission=SupportPermission)
def proposition_support_permission(identity, model, permission):
    # TODO: All users can support propositions at the moment.
    # This must be limited to the users of a department.
    return True


@App.permission_rule(model=Proposition, permission=EditPermission)
def proposition_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


class NewDraftPermission(WritePermission):
    pass


@App.permission_rule(model=Propositions, permission=NewDraftPermission)
def proposition_new_draft_permission(identity, model, permission):
    return identity != NoIdentity


App.path(path='p')(Propositions)


@App.path(
    model=Proposition,
    path="/p/{proposition_id}/{slug}",
    variables=lambda o: dict(proposition_id=o.id, slug=proposition_slug(o))
)
def proposition_path(request, proposition_id=LID(), slug=""):
    proposition = request.q(Proposition).get(proposition_id)

    if proposition is None:
        return None

    canonical_slug = proposition_slug(proposition)
    if canonical_slug == slug:
        return proposition

    canonical = f"/p/{proposition_id}/{canonical_slug}"
    Message.log(msg="redirect to canonical URL", original=slug, canonical=canonical_slug)

    return redirect(canonical)


@App.path(path='/p/{proposition_id}')
class PropositionRedirect:

    def __init__(self, proposition_id=LID()):
        self.id = proposition_id


@App.html(model=Proposition, permission=ViewPermission)
def show(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='discussion')
    return cell.show()


@App.html(model=Proposition, name='associated', permission=ViewPermission)
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

        if relation_type == PropositionRelationType.MODIFIES:
            appstruct['modifies'] = related_proposition
        elif relation_type == PropositionRelationType.REPLACES:
            appstruct['replaces'] = related_proposition
    else:
        # create a new ballot as "container" for the proposition
        area = request.q(SubjectArea).get(appstruct['area_id'])

        if area is None:
            return HTTPBadRequest("area missing")

        if area.department not in request.current_user.departments and not request.identity.has_global_admin_permissions:
            return HTTPBadRequest("area not allowed")

        proposition_type = request.q(PropositionType).get(appstruct['proposition_type_id'])

        if proposition_type is None:
            return HTTPBadRequest("proposition_type missing")

        ballot = Ballot(area=area, proposition_type=proposition_type)

    del appstruct['area_id']
    del appstruct['proposition_type_id']

    proposition = Proposition(
        ballot=ballot, status=PropositionStatus.DRAFT, visibility=PropositionVisibility.HIDDEN, **appstruct
    )

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
def update(self: Proposition, request, appstruct):
    appstruct['tags'] = get_or_create_tags(request.db_session, appstruct['tags'])

    updated_fields = {**appstruct}

    # Dates are required for the following states, set them on state change.
    # This is an admin action only.
    if self.status == PropositionStatus.DRAFT and appstruct["status"] == PropositionStatus.SUBMITTED:
        updated_fields["submitted_at"] = datetime.now()

    if self.status == PropositionStatus.SUBMITTED and appstruct["status"] == PropositionStatus.QUALIFIED:
        updated_fields["qualified_at"] = datetime.now()

    self.update(**updated_fields)
    return redirect(request.link(self))


@App.html(model=Propositions, name='new_draft', permission=NewDraftPermission)
def new_draft(self, request):

    section = self.section
    document = request.q(Document).get(self.document)
    headline, content = get_section_from_document(document, section)
    _ = request.i18n.gettext
    form_data = {
        'document_id': self.document,
        'section': self.section,
        'content': content,
        'title': ' '.join([_("change"), section, headline])
    }
    form = PropositionNewDraftForm(request, request.link(self, name='+new_draft'))
    return PropositionNewDraftCell(request, form, form_data, model=self).show()


@App.html_form_post(
    model=Propositions,
    name='new_draft',
    form=PropositionNewDraftForm,
    cell=PropositionNewDraftCell,
    permission=NewDraftPermission
)
def new_draft_post(self, request, appstruct):
    appstruct['tags'] = get_or_create_tags(request.db_session, appstruct['tags'])
    document = request.q(Document).get(appstruct.pop('document_id'))

    if document.area.department not in request.current_user.departments:
        if not request.identity.has_global_admin_permissions:
            return HTTPBadRequest()

    # create a new ballot as "container" for the proposition
    ballot = Ballot(area=document.area, proposition_type=document.proposition_type)

    section = appstruct.pop('section')
    editing_remarks = appstruct.pop('editing_remarks')

    proposition = Proposition(
        ballot=ballot, status=PropositionStatus.DRAFT, visibility=PropositionVisibility.HIDDEN, **appstruct
    )

    proposition.external_fields = {'external_draft': {'editing_remarks': editing_remarks}}

    changeset = Changeset(document=document, section=section, proposition=proposition)

    request.db_session.add(proposition)
    request.db_session.add(changeset)
    request.db_session.flush()

    return redirect(request.link(proposition))


@App.html(request_method='POST', name='push_draft', permission=EditPermission)
def push_draft(self: Proposition, request: Request):
    """XXX: Supports only Discourse for now.
    A generalized approach like for proposition importers would be nice.
    """

    if 'push_draft' not in request.POST:
        raise HTTPBadRequest()

    exporter_name = self.ballot.area.department.exporter_settings.get('exporter_name')

    if exporter_name is None:
        raise HTTPBadRequest()

    exporter_config = getattr(request.app.settings.exporter, exporter_name)

    self_link = request.link(self)
    editing_remarks = self.external_fields['external_draft']['editing_remarks']

    discourse_content_template = customizable_text(request, 'push_draft_external_template')
    content = discourse_content_template.format(
        draft_link=self_link,
        editing_remarks=editing_remarks,
        abstract=self.abstract,
        content=self.content,
        motivation=self.motivation
    )

    topic = DiscourseTopic(content, self.title, [t.name for t in self.tags])
    discourse_config = DiscourseConfig(**exporter_config)
    resp = create_discourse_topic(discourse_config, topic)
    dd = resp.json()
    portal_content_template = customizable_text(request, 'push_draft_portal_template')
    discourse_topic_url = f'{discourse_config.base_url}/t/{dd["topic_slug"]}/{dd["topic_id"]}'
    self.external_discussion_url = discourse_topic_url
    self.content = portal_content_template.format(topic_url=discourse_topic_url)
    self.motivation = ''
    self.abstract = ''
    self.visibility = PropositionVisibility.PUBLIC
    return redirect(self_link)
