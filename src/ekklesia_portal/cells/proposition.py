from ekklesia_portal.collections.propositions import Propositions
from ekklesia_portal.collections.argument_relations import ArgumentRelations
from ekklesia_portal.database.datamodel import Proposition, Tag, Argument, ArgumentRelation
from ekklesia_portal.forms import PropositionForm
from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.permission import SupportPermission, CreatePermission


class PropositionCell(Cell):
    model = Proposition
    model_properties = ['id', 'title', 'abstract', 'content', 'motivation', 'created_at', 'replacements', 'derivations']

    def associated_url(self):
        return self.link(self._model, 'associated')

    def discussion_url(self):
        return self.link(self._model)

    def is_supported_by_current_user(self):
        return self._model.support_by_user(self.current_user) is not None

    def discussion_link_class(self):
        return 'active' if self.options.get('active_tab') == 'discussion' else ''

    def associated_link_class(self):
        return 'active' if self.options.get('active_tab') == 'associated' else ''

    def new_argument_url(self, argument_type):
        return '#'
        return self.class_link(Argument, dict(argument_type=argument_type), 'new')

    def new_associated_proposition_url(self, association_type):
        return self.class_link(Proposition, dict(association_type=association_type), 'new')

    def new_pro_argument_url(self):
        return self.class_link(ArgumentRelations, dict(proposition_id=self._model.id, relation_type='pro'), '+new')

    def new_con_argument_url(self):
        return self.class_link(ArgumentRelations, dict(proposition_id=self._model.id, relation_type='con'), '+new')

    def supporter_count(self):
        return len(self._model.supporters)

    def support_action(self):
        return self.link(self._model, 'support')

    def pro_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == "pro"]

    def contra_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == "con"]

    def argument_count(self):
        return len(self._model.proposition_arguments)

    def show_support_actions(self):
        return self._request.permitted_for_current_user(self._model, SupportPermission)

    def show_create_argument(self):
        return self._request.permitted_for_current_user(ArgumentRelations(), CreatePermission)


class NewPropositionCell(Cell):
    model = PropositionForm

    def __init__(self, form, request, form_data, collection=None, layout=None, parent=None, template_path=None, **options):
        self.form = form
        self.form_data = form_data or {}
        super().__init__(form, request, collection, layout, parent, template_path, **options)

    def form_html(self):
        return Cell.markup_class(self.form.render(self.form_data))


class PropositionsCell(Cell):
    model = Propositions
    model_properties = ['mode', 'tag', 'search']

    def propositions(self):
        return self._model.propositions(self._request.q)
