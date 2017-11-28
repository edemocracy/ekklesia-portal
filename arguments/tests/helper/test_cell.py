from munch import Munch
from pytest import fixture, raises
from arguments.helper.cell import Cell

@fixture
def model():    
    return Munch(id=5, title="test", private="secret")


@fixture
def cell(model):
    class TestCell(Cell):
        model_properties = ['id', 'title']

    return TestCell(model)


def test_cell_has_model_attributes(cell, model):
    assert cell.id == model.id
    assert cell.title == model.title


def test_cannot_access_private_attr_from_cell(cell, model):
    with raises(AttributeError):
        cell.private
