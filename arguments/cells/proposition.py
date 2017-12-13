from arguments.database.datamodel import Proposition, Argument
from arguments.helper.cell import Cell
from morepath import reify


class PropositionCell(Cell):
    model = Proposition
    model_properties = ['id', 'title', 'content', 'motivation', 'proposition_arguments']

    def new_argument_url(self, argument_type):
        return "#"
        self.class_link(Argument, dict(argument_type=argument_type), 'new')

    @reify
    def supporter_count(self):
        return len(self._model.supporters)

    def arguments(self, argument_type):
        return []
