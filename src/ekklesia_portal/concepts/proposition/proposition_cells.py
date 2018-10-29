import colander
from ekklesia_portal.concepts.argument_relation.argument_relations import ArgumentRelations
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell
from ekklesia_portal.database.datamodel import Proposition, Tag
from ekklesia_portal.enums import ArgumentType
from ekklesia_portal.permission import SupportPermission, CreatePermission
from .propositions import Propositions
from .proposition_helper import items_for_proposition_select_widgets


class PropositionCell(LayoutCell):
    model = Proposition
    model_properties = ['id', 'title', 'abstract', 'content', 'motivation', 'created_at', 'replacements', 'derivations', 'tags']

    def associated_url(self):
        return self.link(self._model, 'associated')

    def discussion_url(self):
        return self.link(self._model)

    def propositions_tag_url(self, tag):
        return self.class_link(Propositions, dict(tag=tag.name))

    def is_supported_by_current_user(self):
        return self._model.support_by_user(self.current_user) is not None

    def discussion_link_class(self):
        return 'active' if self.options.get('active_tab') == 'discussion' else ''

    def associated_link_class(self):
        return 'active' if self.options.get('active_tab') == 'associated' else ''

    def new_associated_proposition_url(self, association_type):
        return self.class_link(Propositions, dict(association_type=association_type), '+new')

    def new_pro_argument_url(self):
        return self.class_link(ArgumentRelations, dict(proposition_id=self._model.id, relation_type=ArgumentType.PRO), '+new')

    def new_con_argument_url(self):
        return self.class_link(ArgumentRelations, dict(proposition_id=self._model.id, relation_type=ArgumentType.CONTRA), '+new')

    def supporter_count(self):
        return self._model.active_supporter_count

    def support_action(self):
        return self.link(self._model, 'support')

    def pro_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == ArgumentType.PRO]

    def contra_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == ArgumentType.CONTRA]

    def argument_count(self):
        return len(self._model.proposition_arguments)

    def show_support_actions(self):
        return self._request.permitted_for_current_user(self._model, SupportPermission)

    def show_create_argument(self):
        return self._request.permitted_for_current_user(ArgumentRelations(), CreatePermission)

    def show_create_associated_proposition(self):
        return self._request.permitted_for_current_user(self._model, CreatePermission)


class NewPropositionCell(NewFormCell):

    def _prepare_form_for_render(self):
        departments = self._request.current_user.departments
        tags = self._request.q(Tag).all()

        if self._form.error is None or self._form.cstruct['tags'] is colander.null:
            selected_tags = None
        else:
            selected_tags = self._form.cstruct['tags'] if self._form.error is not None else None

        items = items_for_proposition_select_widgets(departments, tags, selected_tags)
        self._form.prepare_for_render(items)


class PropositionsCell(LayoutCell):
    model = Propositions
    model_properties = ['mode', 'tag', 'search']

    def propositions(self):
        return list(self._model.propositions(self._request.q))
