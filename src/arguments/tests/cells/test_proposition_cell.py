from pytest import fixture
from arguments.views.proposition import PropositionCell
from arguments.database.datamodel import Argument


@fixture
def proposition_cell(app, proposition):
    return PropositionCell(proposition, None)


def test_proposition_cell(proposition_cell):
    assert proposition_cell.argument_count == 3
    assert len(proposition_cell.pro_arguments) == 2
    assert len(proposition_cell.contra_arguments) == 1
    assert isinstance(proposition_cell.pro_arguments[0], Argument)
    assert isinstance(proposition_cell.contra_arguments[0], Argument)