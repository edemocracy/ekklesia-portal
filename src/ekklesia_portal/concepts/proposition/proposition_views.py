import secrets
from datetime import datetime

import base32_crockford
from ekklesia_common.lid import LID
from ekklesia_common.request import EkklesiaRequest as Request
from eliot import Message, start_action
from datetime import datetime, timezone
from morepath import redirect, Response
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text
from ekklesia_portal.concepts.document.document_helper import get_section_from_document
from ekklesia_portal.concepts.proposition.proposition_permissions import NewDraftPermission, SubmitDraftPermission
from ekklesia_portal.datamodel import Ballot, Changeset, Document, Proposition, PropositionType, SubjectArea, Supporter, SecretVoter
from ekklesia_portal.enums import PropositionRelationType, PropositionStatus, PropositionVisibility, SecretVoterStatus, SupporterStatus
from ekklesia_portal.exporter.discourse import push_draft_to_discourse
from ekklesia_portal.identity_policy import NoIdentity
from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS
from ekklesia_portal.lib.discourse import DiscourseError
from ekklesia_portal.lib.propositions import propositions_to_csv, TableRowOptionalFields
from ekklesia_portal.permission import CreatePermission, EditPermission, SupportPermission, ViewPermission, WritePermission

from .proposition_cells import EditPropositionCell, NewPropositionCell, PropositionCell, PropositionNewDraftCell, PropositionSubmitDraftCell, PropositionsCell
from .proposition_contracts import PropositionEditForm, PropositionNewDraftForm, PropositionNewForm, PropositionSubmitDraftForm
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

    if model.user_is_submitter(identity.user):
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


@App.permission_rule(model=Propositions, permission=NewDraftPermission)
def proposition_new_draft_permission(identity, model, permission):
    return identity != NoIdentity


@App.permission_rule(model=Proposition, permission=SubmitDraftPermission)
def proposition_submit_permission(identity, model: Proposition, permission):
    return model.user_is_submitter(identity.user) or identity.has_global_admin_permissions


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


@App.html(model=Proposition, request_method='POST', name='secret_voting', permission=SupportPermission)
def secret_voting(self, request):
    new_state = request.POST.get("secret_voting")
    if new_state not in ("request", "retract"):
        raise HTTPBadRequest("invalid value for secret_voting or missing")

    user_id = request.current_user.id
    secret_record = request.db_session.query(SecretVoter).filter_by(
        member_id=user_id, ballot_id=self.ballot_id
    ).scalar()
    if secret_record is None:
        secret_record = SecretVoter(member_id=user_id, ballot_id=self.ballot_id)
        request.db_session.add(secret_record)
    if new_state == "request":
        secret_record.status = SecretVoterStatus.ACTIVE
    else:
        secret_record.status = SecretVoterStatus.RETRACTED
    secret_record.last_change = datetime.now(timezone.utc)

    if request.headers.get("HX-Request"):
        return PropositionCell(self, request).secret_voting_action()
    else:
        return redirect(request.link(self))


@App.html(model=Proposition, request_method='POST', name='support', permission=SupportPermission)
def support(self, request):
    new_state = request.POST.get("support")
    if new_state not in ("support", "retract"):
        raise HTTPBadRequest("invalid value for support parameter or missing")

    user_id = request.current_user.id
    supporter = request.db_session.query(Supporter).filter_by(member_id=user_id, proposition_id=self.id).scalar()

    if new_state == "support":

        if supporter is None:
            supporter = Supporter(member_id=user_id, proposition_id=self.id)
            request.db_session.add(supporter)

        supporter.status = SupporterStatus.ACTIVE

    elif supporter is not None:
        supporter.status = SupporterStatus.RETRACTED

    if request.headers.get("HX-Request"):
        cell = PropositionCell(self, request)
        return "\n".join([cell.support_action(), cell.detail_top()])
    else:
        return redirect(request.link(self))


@App.html(request_method='POST', name='become_submitter', permission=SupportPermission)
def become_submitter(self: Proposition, request):
    key_valid = secrets.compare_digest(self.submitter_invitation_key, request.POST.get("submitter_invitation_key", ""))
    if not key_valid:
        raise HTTPBadRequest("wrong submitter invitation key")

    user = request.current_user
    supporter = self.support_by_user(user)

    if supporter is None:
        supporter = Supporter(member=request.current_user, proposition=self)
        request.db_session.add(supporter)

    supporter.submitter = True

    return redirect(request.link(self))


@App.html(model=Propositions)
def index(self, request):
    return PropositionsCell(self, request).show()


@App.view(model=Propositions, media_type="text/csv")
def index_csv(self, request):
    is_global_admin = request.current_user and request.identity.has_global_admin_permissions
    optional_fields = TableRowOptionalFields()
    optional_fields.submitters = is_global_admin
    content = propositions_to_csv(self.propositions(request.q, is_global_admin),
        origin=request.app.settings.common.instance_name, optional_fields=optional_fields)
    response = Response(content, content_type = 'text/csv')
    response.content_disposition = 'attachment; filename="propositions.csv"'
    return response


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


def _create_proposition(request, ballot, appstruct, document=None, section=None):
    appstruct['tags'] = get_or_create_tags(request.db_session, appstruct['tags'])
    editing_remarks = appstruct.pop('editing_remarks')

    submitter_invitation_key = base32_crockford.encode(secrets.randbits(64))

    proposition = Proposition(
        author=request.current_user,
        ballot=ballot,
        status=PropositionStatus.DRAFT,
        submitter_invitation_key=submitter_invitation_key,
        visibility=PropositionVisibility.HIDDEN,
        external_fields={'external_draft': {
            'editing_remarks': editing_remarks
        }},
        **appstruct
    )

    if document is not None and section is not None:
        changeset = Changeset(document=document, section=section, proposition=proposition)
        request.db_session.add(changeset)

    request.db_session.add(proposition)

    is_admin = request.identity.has_global_admin_permissions

    if not is_admin:
        supporter = Supporter(member=request.current_user, proposition=proposition, submitter=True)
        request.db_session.add(supporter)

    request.db_session.flush()
    proposition_url = request.link(proposition)

    exporter_name = ballot.area.department.exporter_settings.get('exporter_name')
    if exporter_name and not is_admin:
        try:
            with start_action(action_type="push_draft", exporter=exporter_name):
                exporter_config = {**getattr(request.app.settings.exporter, exporter_name)}
                external_content_template = customizable_text(request, 'push_draft_external_template')
                portal_content_template = customizable_text(request, 'push_draft_portal_template')
                push_draft_to_discourse(
                    exporter_config, external_content_template, portal_content_template, proposition, proposition_url
                )

        except DiscourseError:
            pass

    return proposition_url


@App.html_form_post(model=Propositions, form=PropositionNewForm, cell=NewPropositionCell, permission=CreatePermission)
def create(self, request, appstruct):
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

    proposition_url = _create_proposition(request, ballot, appstruct)
    return redirect(proposition_url)


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
    document = request.q(Document).get(appstruct.pop('document_id'))

    if document.area.department not in request.current_user.departments:
        if not request.identity.has_global_admin_permissions:
            return HTTPBadRequest()

    # create a new ballot as "container" for the proposition
    ballot = Ballot(area=document.area, proposition_type=document.proposition_type)

    section = appstruct.pop('section')

    proposition_url = _create_proposition(request, ballot, appstruct, document, section)
    return redirect(proposition_url)


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

    exporter_config = {**getattr(request.app.settings.exporter, exporter_name)}
    external_content_template = customizable_text(request, 'push_draft_external_template')
    portal_content_template = customizable_text(request, 'push_draft_portal_template')
    self_link = request.link(self)
    push_draft_to_discourse(exporter_config, external_content_template, portal_content_template, self, self_link)
    return redirect(self_link)


@App.html(name='submit_draft', permission=SubmitDraftPermission)
def submit_draft(self: Proposition, request):

    external_draft_info = self.external_fields.get("external_draft", {})
    importer_name = external_draft_info.get("importer")
    import_info = external_draft_info.get("import_info")

    if external_draft_info:
        if not importer_name:
            raise HTTPBadRequest("should import from external system but importer name is missing")

        if not import_info:
            raise HTTPBadRequest("should import from external system but import info is missing")

        # pre-fill new proposition form from a URL returning data formatted as `from_format`
        # 'for supported formats, see 'PROPOSITION_IMPORT_HANDLERS'
        importer_config = getattr(request.app.settings.importer, importer_name)

        if importer_config is None:
            raise ValueError("unsupported proposition source: " + importer_name)

        import_schema = importer_config['schema']
        import_handler = PROPOSITION_IMPORT_HANDLERS.get(import_schema)
        if import_handler is None:
            raise ValueError("unsupported proposition import schema: " + import_schema)

        form_data = import_handler(importer_config, import_info)
    else:
        form_data = {}

    form = PropositionSubmitDraftForm(request, request.link(self, 'submit_draft_post'))
    return PropositionSubmitDraftCell(self, request, form, form_data).show()


@App.html_form_post(
    model=Proposition,
    name='submit_draft_post',
    form=PropositionSubmitDraftForm,
    cell=PropositionSubmitDraftCell,
    permission=SubmitDraftPermission
)
def submit_draft_post(self: Proposition, request, appstruct):
    if self.status != PropositionStatus.DRAFT:
        raise HTTPBadRequest("status must be DRAFT")

    if not self.ready_to_submit:
        raise HTTPBadRequest("too few submitters")

    self.motivation = appstruct["motivation"]
    self.abstract = appstruct["abstract"]
    self.content = appstruct["content"]
    self.status = PropositionStatus.SUBMITTED
    self.submitted_at = datetime.now()

    return redirect(request.link(self))
