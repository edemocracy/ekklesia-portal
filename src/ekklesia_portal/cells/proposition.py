from ekklesia_portal.database.datamodel import Proposition, Tag, Argument, ArgumentRelation
from ekklesia_portal.helper.cell import Cell


class PropositionCell(Cell):
    model = Proposition
    model_properties = ['id', 'title', 'short', 'content', 'motivation', 'created_at', 'replacements', 'derivations']

    def associated_url(self):
        return self.link(self._model, 'associated')

    def discussion_url(self):
        return self.link(self._model)

    def is_supported_by_current_user(self):
        return self.current_user in self._model.supporters

    def discussion_link_class(self):
        return 'active' if self.options.get('active_tab') == 'discussion' else ''

    def associated_link_class(self):
        return 'active' if self.options.get('active_tab') == 'associated' else ''

    def new_argument_url(self, argument_type):
        return "#"
        self.class_link(Argument, dict(argument_type=argument_type), 'new')

    def new_associated_proposition_url(self, association_type):
        return "#"
        self.class_link(Proposition, dict(association_type=association_type), 'new')

    def supporter_count(self):
        return len(self._model.supporters)

    def pro_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == "pro"]

    def contra_argument_relations(self):
        return [p for p in self._model.proposition_arguments if p.argument_type == "con"]

    def argument_count(self):
        return len(self._model.proposition_arguments)
