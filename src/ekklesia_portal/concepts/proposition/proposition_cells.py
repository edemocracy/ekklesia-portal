from operator import attrgetter
import urllib.parse
import colander
import copy
from eliot import log_call
from ekklesia_portal.app import App
from ekklesia_portal.concepts.argument_relation.argument_relations import ArgumentRelations
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell
from ekklesia_portal.database.datamodel import Department, Proposition, Tag, PropositionNote, VotingPhase, PropositionType
from ekklesia_common.translation import _
from ekklesia_common.cell import Cell
from ekklesia_portal.enums import ArgumentType, PropositionStatus, OpenSlidesVotingResult
from ekklesia_portal.permission import SupportPermission, CreatePermission, EditPermission
from .propositions import Propositions
from .proposition_helper import items_for_proposition_select_widgets


@App.cell(Proposition)
class PropositionCell(LayoutCell):

    model_properties = [
        'abstract',
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
        'replacements',
        'replaces',
        'tags',
        'title'
    ]

    actions = Cell.fragment('proposition_actions')
    tabs = Cell.fragment('proposition_tabs')
    small = Cell.fragment('proposition_small')
    card = Cell.fragment('proposition_card')

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
        template = f"proposition/proposition_status_{variant}.j2.jade"
        return self.render_template(template)

    @Cell.fragment
    def history(self):
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
        template = f"proposition/proposition_history_{variant}.j2.jade"
        return self.render_template(template)

    def associated_url(self):
        return self.link(self._model, 'associated')

    def report_url(self):
        return self._s.app.report_url

    def share_url(self):
        if self._app.settings.share.use_url_shortener:
            from ekklesia_portal.helper.url_shortener import make_tiny
            return make_tiny(self.self_link)
        else:
            return self.self_link[:69]

    @log_call
    def share_email_url(self):
        share_email_topic = (self._s.share.email_topic[self.language]
                             .format(
                                 voting_identifier=self._model.voting_identifier,
                                 title=self._model.title[:140]))

        share_email_body = self._s.share.email_body[self.language] + self.share_url
        email_url = urllib.parse.urlencode({'subject': share_email_topic,
                                            'body': share_email_body},
                                           quote_via=urllib.parse.quote)
        email_url = 'mailto:?' + email_url
        return email_url

    @log_call
    def share_twitter_url(self):
        share_tweet_msg = (self._s.share.tweet_msg[self.language]
                           .format(
                               voting_identifier=self._model.voting_identifier,
                               title=self._model.title[:70]))

        twitter_url = urllib.parse.urlencode({'hashtags': self._app.settings.share.hashtag,
                                              'related': self._app.settings.share.promote_account,
                                              'text': share_tweet_msg,
                                              'tw_p': 'tweetbutton',
                                              'url': self.share_url})
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
        return self.link(self._model)

    def propositions_tag_url(self, tag):
        return self.class_link(Propositions, dict(tag=tag.name))

    def is_supported_by_current_user(self):
        if self.current_user is None:
            return False
        return self._model.support_by_user(self.current_user) is not None

    def discussion_link_class(self):
        return 'active' if self.options.get('active_tab') == 'discussion' else ''

    def associated_link_class(self):
        return 'active' if self.options.get('active_tab') == 'associated' else ''

    def new_associated_proposition_url(self, association_type):
        return self.class_link(Propositions, dict(association_type=association_type), '+new')

    def new_pro_argument_url(self):
        return self.class_link(
            ArgumentRelations,
            dict(proposition_id=self._model.id, relation_type=ArgumentType.PRO.name),
            '+new')

    def new_con_argument_url(self):
        return self.class_link(
            ArgumentRelations,
            dict(proposition_id=self._model.id, relation_type=ArgumentType.CONTRA.name),
            '+new')

    def supporter_count(self):
        return self._model.active_supporter_count

    def support_action(self):
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
        else:
            return self._model.title

    def show_support_actions(self):
        return self._request.permitted_for_current_user(self._model, SupportPermission)

    def show_create_argument(self):
        return self._request.permitted_for_current_user(ArgumentRelations(), CreatePermission)

    def show_create_associated_proposition(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)

    def voting_phase(self):
        return self._model.ballot.voting

    def voting_result_state(self):
        result = self._model.ballot.result
        if result:
            try:
                return OpenSlidesVotingResult(result.get(self._model.voting_identifier, {}).get("state"))
            except ValueError:
                return

    def voting_result_symbol(self):
        symbols = {
            OpenSlidesVotingResult.ACCEPTED: "fas fa-check",
            OpenSlidesVotingResult.REJECTED: "fas fa-ban",
            OpenSlidesVotingResult.NOT_DECIDED: "fas fa-spinner"
        }
        return symbols.get(self.voting_result_state)

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)

    def edit_url(self):
        return self.link(self._model, 'edit')

    def note_url(self):
        if self.current_user is None:
            return False
        return self.class_link(
            PropositionNote,
            variables={'proposition_id': self._model.id, 'user_id': self._request.current_user.id},
            name='edit')

    def show_full_history(self):
        return self.options.get('show_details')

@App.cell(Propositions, 'new')
class NewPropositionCell(NewFormCell):

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

        items = items_for_proposition_select_widgets(departments, tags, selected_tag_names)
        self._form.prepare_for_render(items)


class EditPropositionCell(EditFormCell):

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
        items = items_for_proposition_select_widgets(departments, tags, selected_tag_names)
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


@App.cell(Propositions)
class PropositionsCell(LayoutCell):

    model_properties = ['mode', 'tag', 'search', 'phase', 'type', 'status', 'department', 'subject_area']

    def propositions(self):
        return list(self._model.propositions(self._request.q))

    def link_remove_filter(self, filter):
        proposition = copy.copy(self._model)
        setattr(proposition, filter, None)
        return self.link(proposition)

    def voting_phase_title(self, phase):
        voting_phase = self._request.q(VotingPhase).filter_by(name=phase).scalar()
        if voting_phase is None:
            return phase
        else:
            return voting_phase.title

    def proposition_type_name(self, type):
        proposition_type = self._request.q(PropositionType).filter_by(abbreviation=type).scalar()
        if proposition_type is None:
            return type
        else:
            return proposition_type.name
