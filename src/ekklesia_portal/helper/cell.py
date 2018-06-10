import jinja2
from ekklesia_portal.helper.utils import cached_property
from markupsafe import Markup


_cell_registry = {}


def find_cell_by_model_instance(model):
    return _cell_registry[model.__class__]


class CellMeta(type):
    """
    Registers Cell types that are bound to a Model class.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        if cls.model:
            _cell_registry[cls.model] = cls
        return super().__init__(name, bases, attrs)


class Cell(metaclass=CellMeta):
    """
    View model base class which is basically a wrapper around a template.
    Templates can access attributes of the cell and some selected model properties directly.
    """
    model = None
    model_properties = []
    layout = True
    #: class that should be used to mark safe HTML output
    markup_class = Markup

    def __init__(self, model, request, collection=None, layout=None, template_path=None, **options):
        self._model = model
        self._request = request
        self.current_user = request.current_user
        self._app = request.app
        self.collection = collection
        self._template_path = template_path
        self.options = options
        if layout is not None:
            self.layout = layout

    @property
    def template_path(self):
        if self._template_path is None:
            name = self._model.__class__.__name__.lower()
            self._template_path = name + ".j2.jade"

        return self._template_path

    def render_template(self, template_path):
        return self.__class__.markup_class(self._request.render_template(template_path, _cell=self))

    def show(self):
        return self.render_template(self.template_path)

    # template helpers

    def link(self, model, name='', *args, **kwargs):
        return self._request.link(model, name, *args, **kwargs)

    def class_link(self, model_class, variables, name='', *args, **kwargs):
        return self._request.class_link(model_class, variables, name, *args, **kwargs)

    def cell(self, model, layout=False, view_name='', **options):
        """Look up a cell by model and create an instance.
        Cells created with this method are rendered without layout by default.
        """
        cell_class = find_cell_by_model_instance(model)
        return cell_class(model, self._request, layout=layout, **options)

    def render_cell(self, model=None, collection=None, separator=None, layout=False, view_name='', **options):
        """Look up a cell by model and render it to HTML.
        Cells are rendered without layout by default.
        """
        if collection is not None:
            if model is not None:
                raise ValueError("model and collection arguments cannot be used together!")

            parts = [self.cell(item, layout=layout, **options).show() for item in collection]

            if separator is None:
                separator = "\n"

            return self.__class__.markup_class(separator.join(parts))

        else:
            return self.cell(model, layout=layout, **options).show()

    @cached_property
    def self_link(self):
        return self.link(self._model)

    # magic starts here...

    def __getattr__(self, name):
        if name in self.model_properties:
            return getattr(self._model, name)

        raise AttributeError()

    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)

        if name in self.model_properties:
            return getattr(self._model, name)

        raise KeyError()

    def __contains__(self, name):
        return name in self.model_properties or hasattr(self, name)


class JinjaCellContext(jinja2.runtime.Context):
    """
    Custom jinja context with the ability to look up template variables in a cell (view model)
    """

    def __init__(self, environment, parent, name, blocks):
        super().__init__(environment, parent, name, blocks)
        self._cell = parent.get('_cell')

    def resolve_or_missing(self, key):
        if self._cell is not None:
            if key == "_request":
                return self._cell._request

            if key in self._cell:
                return self._cell[key]

        return super().resolve_or_missing(key)

    def __contains__(self, name):
        if self._cell and name in self._cell:
            return True

        return super().__contains__(name)


class JinjaCellEnvironment(jinja2.Environment):
    """
    Example jinja environment class which uses the JinjaCellContext
    """
    context_class = JinjaCellContext
