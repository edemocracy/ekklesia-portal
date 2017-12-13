from arguments.helper.cell import Cell
from arguments.collections.propositions import Propositions


class PropositionsCell(Cell):
    model = Propositions
    model_properties = ['mode', 'tag', 'searchterm']

    @property
    def propositions(self):
        return self._model.propositions(self._request.q)
