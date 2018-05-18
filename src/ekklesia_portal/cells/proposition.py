from ekklesia_portal.database.datamodel import Proposition, Tag, Argument, ArgumentRelation
from ekklesia_portal.helper.cell import Cell
from morepath import reify


class PropositionCell(Cell):
    model = Proposition
    model_properties = ['id', 'title', 'content', 'motivation', 'created_at']

    @reify
    def is_supported_by_current_user(self):
        return self.current_user in self._model.supporters


    def new_argument_url(self, argument_type):
        return "#"
        self.class_link(Argument, dict(argument_type=argument_type), 'new')

    @reify
    def supporter_count(self):
        return len(self._model.supporters)

    @reify
    def pro_arguments(self):
        return [p.argument for p in self._model.proposition_arguments if p.argument_type == "pro"]

    @reify
    def contra_arguments(self):
        return [p.argument for p in self._model.proposition_arguments if p.argument_type == "con"]

    @reify
    def argument_count(self):
        return len(self._model.proposition_arguments)
