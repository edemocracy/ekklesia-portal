from unittest.mock import MagicMock
from munch import Munch
from pytest import fixture, raises
import ekklesia_portal.helper.cell
from ekklesia_portal.helper.cell import Cell, JinjaCellEnvironment
from ekklesia_portal.app import make_jinja_env
from ekklesia_portal.request import EkklesiaPortalRequest
from webob.request import BaseRequest


@fixture
def model():
    class TestModel(Munch):
        pass

    return TestModel(id=5, title="test", private="secret")


@fixture
def request_for_cell(app):
    environ = BaseRequest.blank('test').environ
    return MagicMock(spec=EkklesiaPortalRequest(environ, app))


@fixture
def jinja_env(app):
    import jinja2
    template_loader = jinja2.loaders.PackageLoader("tests")
    return make_jinja_env(jinja_environment_class=JinjaCellEnvironment, jinja_options=dict(loader=template_loader), app=app)


@fixture
def render_template(jinja_env):
    def render_template(template, **context):
        template = jinja_env.get_template(template)
        return template.render(**context)

    return render_template


@fixture
def cell(model, request_for_cell):
    _model = model

    class DummyMarkup(str):
        def __init__(self, content):
            self.content = content

    class TestCell(Cell):
        model = _model.__class__
        model_properties = ['id', 'title']
        markup_class = DummyMarkup

        @property
        def test_url(self):
            return "https://example.com/test"

    return TestCell(model, request_for_cell)


def test_cell_is_registrated(cell, model):
    assert model.__class__ in ekklesia_portal.helper.cell._cell_registry


def test_cell_cell(cell, model):
    another_cell = cell.cell(model)
    assert another_cell.__class__ == cell.__class__


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
    assert res.content.render_template.called_with(cell.template_path, cell)


def test_cell_render_cell(cell, model):
    res = cell.render_cell(model, some_option=42)
    assert res.content.render_template.called_with(model, cell._request, some_option=42)


def test_cell_render_cell_collection(cell, model):
    model2 = model.copy()
    model2.title = "test2"
    models = [model, model2]
    cell.render_template = MagicMock()
    cell.render_cell(collection=models, some_option=42)
    assert cell.render_template.called_with(model, cell._request, some_option=42)
    assert cell.render_template.called_with(model2, cell._request, some_option=42)


def test_cell_render_cell_model_and_collection_not_allowed(cell, model):
    with raises(ValueError):
        cell.render_cell(model, collection=[], some_option=42)


def test_cell_jinja_integration(cell, model, render_template, request_for_cell):

    request_for_cell.render_template.side_effect = render_template
    res = cell.show()
    assert str(model.id) in res.content
    assert model.title in res.content
