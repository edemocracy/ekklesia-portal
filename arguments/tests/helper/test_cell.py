from unittest.mock import MagicMock
from munch import Munch
from pytest import fixture, raises
from arguments.helper.cell import Cell, JinjaCellEnvironment
from arguments.app import make_jinja_env, CustomRequest
from webob.request import BaseRequest

@fixture
def model():    
    class TestModel(Munch):
        pass
    
    return TestModel(id=5, title="test", private="secret")

@fixture
def request_for_cell(app):
    environ = BaseRequest.blank('test').environ
    return MagicMock(spec=CustomRequest(environ, app))


@fixture
def jinja_env():
    import jinja2
    template_loader = jinja2.loaders.PackageLoader("arguments.tests")
    return make_jinja_env(jinja_environment_class=JinjaCellEnvironment, jinja_options=dict(loader=template_loader))


@fixture
def render_template(jinja_env):
    def render_template(template, **context):
        template = jinja_env.get_template(template)
        return template.render(**context)
        
    return render_template

@fixture
def cell(model, request_for_cell):
    class TestCell(Cell):
        model_properties = ['id', 'title']
        
        @property
        def test_url(self):
            return "https://example.com/test"


    return TestCell(model, request_for_cell)


def test_cell_getattr(cell, model):
    assert cell.id == model.id
    assert cell.title == model.title


def test_cell_getitem(cell, model):
    assert cell["id"] == model.id
    assert cell["title"] == model.title
    assert cell["test_url"] == cell.test_url


def test_cell_contains(cell, model):
    assert "id" in cell
    assert "title" in cell
    assert "test_url" in cell
    
    
def test_cell_attrs_override_model_attrs(cell, model):
    cell.id = 42
    assert cell["id"] == 42


def test_cannot_access_private_attr_from_cell(cell, model):
    with raises(AttributeError):
        cell.private


def test_cell_template_path(cell, model):
    assert cell.template_path == "testmodel.j2.jade"
    
    
def test_cell_show(cell, model):
    res = cell.show()
    assert res.render_template.called_with(cell.template_path, cell)
    
    
def test_cell_jinja_integration(cell, model, render_template, request_for_cell):

    request_for_cell.render_template.side_effect = render_template
    res = cell.show()
    assert str(model.id) in res
    assert model.title in res
    
    