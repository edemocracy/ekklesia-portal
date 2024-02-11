import urllib.parse
import math
from operator import attrgetter
from secrets import compare_digest

import colander
from ekklesia_common.cell import Cell
from functools import cached_property
from eliot import log_call
from sqlalchemy import func

from ekklesia_common.lid import LID
from ekklesia_portal.app import App
from ekklesia_portal.concepts.argument_relation.argument_relations import ArgumentRelations
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition.proposition_permissions import SubmitDraftPermission
from ekklesia_portal.datamodel import Department, Document, Proposition, PropositionNote, PropositionType, Tag, VotingPhase, SecretVoter
from ekklesia_portal.helper.url_shortener import make_tiny
from ekklesia_portal.enums import ArgumentType, OpenSlidesVotingResult, PropositionStatus, SecretVoterStatus
from ekklesia_portal.lib.url import url_change_query
from ekklesia_portal.permission import CreatePermission, EditPermission, SupportPermission

from .proposition_helper import items_for_proposition_select_widgets
from .propositions import Propositions

@App.cell()
class PropositionCell(LayoutCell):

    _model: Proposition

    model_properties = [
        'abstract',
        'author',
        'ballot',
        'content',
        'created_at',
        'submitted_at',
        'qualified_at',
        'derivations',
        'external_discussion_url',
        'id',
        'modifies',
        'motivation',
        'qualification_quorum',
        'replacements',
        'replaces',
        'submitter_invitation_key',
        'tags',
        'title',
        'secret_voters_count',
        'secret_voters_user_count',
        'secret_voting_quorum',
    ]

    actions = Cell.fragment('proposition_actions')
    secret_voting = Cell.template_fragment('proposition_secret_voting')
    support = Cell.template_fragment('proposition_support')
    tabs = Cell.fragment('proposition_tabs')
    badges = Cell.fragment('proposition_badges')
    small = Cell.fragment('proposition_small')
    card = Cell.fragment('proposition_card')

    @Cell.fragment
    def tab_content(self):
        variant = self.options.get("active_tab")
        if variant is None:
            return ""
        template = f"proposition/tab/proposition_tab_{variant}.j2.jade"
        return self.render_template(template)

    @Cell.fragment
    def status(self):
        status_to_variant = {
            PropositionStatus.DRAFT: 'draft',
            PropositionStatus.CHANGING: 'submitted',
            PropositionStatus.SUBMITTED: 'submitted',
            PropositionStatus.ABANDONED: 'submitted',
            PropositionStatus.QUALIFIED: 'submitted',
            PropositionStatus.SCHEDULED: 'scheduled',
            PropositionStatus.VOTING: 'scheduled',
            PropositionStatus.FINISHED: 'finished',
        }
        variant = status_to_variant[self._model.status]
        template = f"proposition/status/proposition_status_{variant}.j2.jade"
        return self.render_template(template)

    @Cell.fragment
    def history(self):
        status_to_variant = {
            PropositionStatus.DRAFT: 'draft',
            PropositionStatus.CHANGING: 'submitted',
            PropositionStatus.SUBMITTED: 'submitted',
            PropositionStatus.ABANDONED: 'submitted',
            PropositionStatus.QUALIFIED: 'qualified',
            PropositionStatus.SCHEDULED: 'scheduled',
            PropositionStatus.VOTING: 'voting',
            PropositionStatus.FINISHED: 'finished',
        }
        variant = status_to_variant[self._model.status]
        template = f"proposition/history/proposition_history_{variant}.j2.jade"
        return self.render_template(template)

    @Cell.fragment
    def detail_top(self):
        variant = self._model.status
        if variant not in (PropositionStatus.DRAFT, PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED,
                           PropositionStatus.SCHEDULED):
            return ""
        template = f"proposition/detail_top/proposition_detail_top_{variant}.j2.jade"
        return self.render_template(template)

    def department_name(self):
        return self._model.ballot.area.department.name

    def subject_area_name(self):
        return self._model.ballot.area.name

    def associated_url(self):
        return self.link(self._model, 'associated') + "#bottom"

    def report_url(self):
        return self._s.app.report_url

    def share_url(self):
        if self._app.settings.share.use_url_shortener:
            return make_tiny(self.self_link)

        return self.self_link[:69]

    @log_call
    def share_email_url(self):
        share_email_topic = (
            self._s.share.email_topic[
                self.language].format(voting_identifier=self._model.voting_identifier, title=self._model.title[:140])
        )

        share_email_body = self._s.share.email_body[self.language] + self.share_url
        email_url = urllib.parse.urlencode({
            'subject': share_email_topic,
            'body': share_email_body
        },
                                           quote_via=urllib.parse.quote)
        email_url = 'mailto:?' + email_url
        return email_url

    @log_call
    def share_twitter_url(self):
        share_tweet_msg = (
            self._s.share.tweet_msg[
                self.language].format(voting_identifier=self._model.voting_identifier, title=self._model.title[:70])
        )

        twitter_url = urllib.parse.urlencode({
            'hashtags': self._app.settings.share.hashtag,
            'related': self._app.settings.share.promote_account,
            'text': share_tweet_msg,
            'tw_p': 'tweetbutton',
            'url': self.share_url
        })
        twitter_url = 'https://twitter.com/intent/tweet?' + twitter_url
        return twitter_url

    def ballot_url(self):
        return self.link(self._model.ballot)

    def ballot_title(self):
        ballot = self._model.ballot
        if ballot.name:
            return ballot.name

        return f'# {ballot.id}'

    def discussion_url(self):
        return self.link(self._model) + "#bottom"

    def propositions_badge_url(self, department_name, subject_area_name=None, tag_name=None):
        params = {"department": department_name}

        if subject_area_name:
            params["subject_area"] = subject_area_name

        if tag_name:
            params["tags"] = tag_name

        return self.class_link(Propositions, params)

    def current_user_is_supporter(self):
        if self.current_user is None:
            return False
        return self._model.support_by_user(self.current_user) is not None

    def current_user_is_submitter(self):
        if self.current_user is None:
            return False
        return self._model.user_is_submitter(self.current_user)

    def current_user_is_author(self):
        if self.current_user is None:
            return False
        return self._model.author == self.current_user

    def discussion_link_class(self):
        return 'active' if self.options.get('active_tab') == 'discussion' else ''

    def associated_link_class(self):
        return 'active' if self.options.get('active_tab') == 'associated' else ''

    def new_amendment_url(self):
        return self.link(self._model, '+new_amendment')

    def new_counter_proposition_url(self):
        return self.class_link(Propositions, dict(association_type="counter", association_id=self._model.id.repr), '+new')

    def new_pro_argument_url(self):
        return self.class_link(
            ArgumentRelations, dict(proposition_id=self._model.id, relation_type=ArgumentType.PRO.name), '+new'
        )

    def new_con_argument_url(self):
        return self.class_link(
            ArgumentRelations, dict(proposition_id=self._model.id, relation_type=ArgumentType.CONTRA.name), '+new'
        )

    def missing_submitters_count(self):
        return self._model.ballot.proposition_type.policy.submitter_minimum - self._model.submitter_count

    def supporter_count(self):
        return self._model.active_supporter_count

    def become_submitter_action(self):
        return self.link(self._model, 'become_submitter')

    def secret_voting_url(self):
        return self.link(self._model, 'secret_voting')

    def support_url(self):
        return self.link(self._model, 'support')

    def pro_argument_relations(self):
        relations = [p for p in self._model.proposition_arguments if p.argument_type == ArgumentType.PRO]
        return sorted(relations, key=attrgetter('score'), reverse=True)

    def contra_argument_relations(self):
        relations = [p for p in self._model.proposition_arguments if p.argument_type == ArgumentType.CONTRA]
        return sorted(relations, key=attrgetter('score'), reverse=True)

    def argument_count(self):
        return len(self._model.proposition_arguments)

    def full_title(self):
        if self._model.voting_identifier:
            return self._model.voting_identifier + ': ' + self._model.title

        return self._model.title

    def ready_to_submit(self):
        return self._model.ready_to_submit

    def show_support(self):
        return self._model.status in (PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED)

    def can_support(self):
        return self.show_support and self._request.permitted_for_current_user(self._model, SupportPermission)

    def supporter_quorum_percent(self):
        if self._model.qualification_quorum > 0:
            return self._model.active_supporter_count / self._model.qualification_quorum * 100

    def show_secret_voting(self):
        return self._model.status in (
            PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED, PropositionStatus.SCHEDULED
        ) and self._model.secret_voting_quorum > 0 and self._request.permitted_for_current_user(
            self._model, SupportPermission
        )

    def can_request_secret_voting(self):
        return self.show_secret_voting and self._request.permitted_for_current_user(self._model, SupportPermission)

    def show_submit_draft_action(self):
        return self._model.ready_to_submit and self._request.permitted_for_current_user(
            self._model, SubmitDraftPermission
        )

    def show_create_argument(self):
        return self._model.status in (
            PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED, PropositionStatus.SCHEDULED,
            PropositionStatus.VOTING, PropositionStatus.ABANDONED
        ) and self._request.permitted_for_current_user(ArgumentRelations(), CreatePermission)

    def show_goto_arguments(self):
        return self._model.status in (
            PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED, PropositionStatus.SCHEDULED,
            PropositionStatus.VOTING, PropositionStatus.ABANDONED
        )

    def show_create_amendment(self):
        return self._s.app.enable_amendments and self._model.status in (
            PropositionStatus.DRAFT, PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED,
            PropositionStatus.SCHEDULED
        ) and self._request.permitted_for_current_user(Proposition(), CreatePermission) and self._model.modifies is None

    def show_create_counter_proposition(self):
        return self._s.app.enable_counter_propositions and self._model.status in (
            PropositionStatus.DRAFT, PropositionStatus.SUBMITTED, PropositionStatus.QUALIFIED,
            PropositionStatus.SCHEDULED
        ) and self._request.permitted_for_current_user(Propositions(), CreatePermission) and self._model.modifies is None

    def show_submitter_names(self):
        if self.current_user is None:
            return False

        if self._model.ballot.area.department in self.current_user.managed_departments:
            return True

        if self._request.identity.has_global_admin_permissions:
            return True

        if self._model.user_is_submitter(self.current_user):
            return True

        if self._model.author == self.current_user:
            return True

        return False

    def valid_submitter_invitation_key(self):
        key = self._request.GET.get("submitter_invitation_key")
        if key is None:
            return False
        return compare_digest(self._model.submitter_invitation_key, key)

    def voting_phase(self):
        return self._model.ballot.voting

    def voting_result_state(self):
        result = self._model.ballot.result
        if result:
            try:
                return OpenSlidesVotingResult(result.get(self._model.voting_identifier, {}).get("state"))
            except ValueError:
                pass

        return None

    def voting_result_symbol(self):
        symbols = {
            OpenSlidesVotingResult.ACCEPTED: "fas fa-check",
            OpenSlidesVotingResult.REJECTED: "fas fa-ban",
            OpenSlidesVotingResult.NOT_DECIDED: "fas fa-spinner"
        }
        return symbols.get(self.voting_result_state)

    def show_edit_button(self):
        return self._request.permitted_for_current_user(self._model, EditPermission)

    def submit_draft_url(self):
        return self.link(self._model, 'submit_draft')

    def edit_url(self):
        return self.link(self._model, 'edit')

    def note_url(self):
        if self.current_user is None:
            return False
        return self.class_link(
            PropositionNote,
            variables={
                'proposition_id': self._model.id,
                'user_id': self._request.current_user.id
            },
            name='edit'
        )

    def become_submitter_url(self):
        return self.self_link + f"?submitter_invitation_key={self._model.submitter_invitation_key}"

    def submitter_names(self):
        return [pm.member.name for pm in self._model.propositions_member if pm.submitter]

    def show_full_history(self):
        return self.options.get('show_details')

    def secret_voting_requested(self):
        user_id = None
        if self.current_user is not None:
            user_id = self.current_user.id
        secret_record = self._request.db_session.query(SecretVoter).filter_by(
            member_id=user_id, ballot_id=self._model.ballot_id
        ).scalar()

        if secret_record is None:
            return False

        return secret_record.status == SecretVoterStatus.ACTIVE


@App.cell()
class NewPropositionCell(NewFormCell):

    _model: Propositions

    def _prepare_form_for_render(self):
        if self._request.identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = self._request.current_user.departments

        tags = self._request.q(Tag).all()

        if self._form.error is None or self._form.cstruct['tags'] is colander.null:
            selected_tag_names = None
        else:
            selected_tag_names = self._form.cstruct['tags']

        proposition_types = self._request.q(PropositionType)
        items = items_for_proposition_select_widgets(departments, tags, proposition_types, selected_tag_names)
        self._form.prepare_for_render(items)

    def relation_type(self):
        if self._form_data and "relation_type" in self._form_data:
            return self._form_data["relation_type"]
        else:
            return None

    @cached_property
    def relation(self):
        if self._form_data and "related_proposition_id" in self._form_data:
            return self._request.q(Proposition).get(LID.from_str(self._form_data["related_proposition_id"]))
        else:
            return None

    def relation_url(self):
        return self.link(self.relation) if self.relation else ""

    def relation_name(self):
        return self.relation.title if self.relation else ""


@App.cell()
class EditPropositionCell(EditFormCell):

    _model: Proposition

    def _prepare_form_for_render(self):
        if self._form.error is None:
            form_data = self._model.to_dict()
            form_data['area_id'] = self._model.ballot.area_id
            form_data['tags'] = [t.name for t in self._model.tags]
            self.set_form_data(form_data)
            selected_tag_names = None
        else:
            selected_tag_names = self._form.cstruct['tags']

        if self._request.identity.has_global_admin_permissions:
            departments = self._request.q(Department)
        else:
            departments = self._request.current_user.departments

        tags = self._request.q(Tag).all()
        items = items_for_proposition_select_widgets(departments, tags, selected_tags=selected_tag_names)
        self._form.prepare_for_render(items)

    def department_name(self):
        return self._model.ballot.area.department.name

    def subject_area_name(self):
        return self._model.ballot.area.name

    def ballot_id(self):
        return self._model.ballot.id

    def ballot_name(self):
        return self._model.ballot.name

    def ballot_url(self):
        return self.link(self._model.ballot)

    def become_submitter_url(self):
        return self.self_link + f"?submitter_invitation_key={self._model.submitter_invitation_key}"

    def show_push_draft(self):
        exporter_name = self._model.ballot.area.department.exporter_settings.get('exporter_name')
        return exporter_name and self._model.status == PropositionStatus.DRAFT

    def push_draft_action(self):
        return self.link(self._model, 'push_draft')

    def exporter_description(self):
        return self._model.ballot.area.department.exporter_settings.get('exporter_description', '')


@App.cell()
class PropositionsCell(LayoutCell):

    _model: Propositions

    model_properties = [
        'department',
        'phase',
        'search',
        'section',
        'sort',
        'status_values',
        'subject_area',
        'tag_values',
        'type',
        'without_tag_values',
        'only_supporting'
    ]

    pager = Cell.fragment("propositions_pager")

    def propositions(self):
        is_admin = self.current_user and self._request.identity.has_global_admin_permissions
        return list(self._model.propositions(self._request.q, self.current_user, is_admin))

    def prop_count(self):
        is_admin = self.current_user and self._request.identity.has_global_admin_permissions
        return self._model.propositions(self._request.q, self.current_user, is_admin, count=True)

    def page_count(self):
        per_page = self.prop_per_page
        if per_page <= 0:
            return -1
        else:
            return int(math.ceil(self.prop_count / per_page))

    def prop_per_page(self):
        return self._model.propositions_per_page()

    def page(self):
        return self._model.page or 1

    # Overrides the base method in LayoutCell
    def search_query(self):
        return self._model.build_search_query()

    def change_self_link(self, **kwargs):
        propositions = self._model.replace(**kwargs)
        return self.link(propositions)

    def voting_phase_title(self, phase):
        voting_phase = self._request.q(VotingPhase).filter(func.lower(VotingPhase.name) == func.lower(phase)).scalar()
        if voting_phase is None:
            return phase

        return voting_phase.title

    def proposition_type_name(self, proposition_type):
        proposition_type = self._request.q(PropositionType).filter(
            func.lower(PropositionType.abbreviation) == func.lower(proposition_type)
        ).scalar()
        if proposition_type is None:
            return proposition_type

        return proposition_type.name

    def visibility_values(self):
        if self.current_user and self._request.identity.has_global_admin_permissions:
            return self._model.visibility_values
        else:
            return None

    def export_csv_url(self):
        return url_change_query(self.self_link, media_type="text/csv")


@App.cell('new_draft')
class PropositionNewDraftCell(NewFormCell):

    _model: Propositions

    def _prepare_form_for_render(self):
        tags = self._request.q(Tag).all()
        items = items_for_proposition_select_widgets([], tags)
        self._form.prepare_for_render(items)

    @cached_property
    def _document(self):
        return self._request.q(Document).get(self._model.document)

    def department_name(self):
        return self._document.area.department.name

    def document_name(self):
        return self._document.name

    def explanation(self):
        return customizable_text(self._request, 'new_draft_explanation')


@App.cell('submit_draft')
class PropositionSubmitDraftCell(EditFormCell):

    _model: Proposition

    def _prepare_form_for_render(self):
        if self._form.error is None:
            data_from_model = self._model.to_dict()
            data_from_model['tags'] = [t.name for t in self._model.tags]
            # Override fields from the model with the given form data
            form_data = {**data_from_model, **self._form_data}
            self.set_form_data(form_data)
            selected_tag_names = None
        else:
            selected_tag_names = self._form.cstruct['tags']

        tags = self._request.q(Tag).all()
        items = items_for_proposition_select_widgets([], tags, selected_tags=selected_tag_names)
        self._form.prepare_for_render(items)

    def department_name(self):
        return self._model.ballot.area.department.name

    def subject_area_name(self):
        return self._model.ballot.area.name

    def proposition_type_name(self):
        return self._model.ballot.proposition_type.name

    def explanation(self):
        return customizable_text(self._request, 'submit_draft_explanation')

    def draft_not_fully_matched(self):
        return not self._form_data.get("all_matched")

@App.cell('new_amendment')
class NewPropositionAmendmentCell(NewFormCell):

    _model: Proposition
    model_properties = ["title"]

    def new_amendment_explanation(self):
        return customizable_text(self._request, 'new_proposition_amendment_explanation')
