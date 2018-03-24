from unittest.mock import Mock
from pytest import fixture
from ekklesia_portal.views.proposition import PropositionCell
from ekklesia_portal.database.datamodel import Argument


@fixture
def proposition_cell(app, proposition):
    return PropositionCell(proposition, Mock())


def test_proposition_cell(proposition_cell):
    assert proposition_cell.argument_count == 3
    assert len(proposition_cell.pro_arguments) == 2
    assert len(proposition_cell.contra_arguments) == 1
    assert isinstance(proposition_cell.pro_arguments[0], Argument)
    assert isinstance(proposition_cell.contra_arguments[0], Argument)