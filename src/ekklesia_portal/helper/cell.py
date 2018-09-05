from __future__ import annotations
from webob import Request
from typing import Any, Iterable, Dict, Type, ClassVar
import case_conversion
import inspect
import jinja2
from ekklesia_portal.helper.utils import cached_property
from markupsafe import Markup


_cell_registry: Dict[Any, Cell] = {}


def find_cell_by_model_instance(model) -> Cell:
    return _cell_registry[model.__class__]


class CellMeta(type):
    """
    Registers Cell types that are bound to a Model class.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        model = getattr(cls, 'model', None)
        if model:
            _cell_registry[model] = cls
        if 'template_prefix' not in cls.__dict__:
            module_path = cls.__module__.split('.')
            if module_path[1] == 'concepts':
                cls.template_prefix = module_path[2]
            else:
                cls.template_prefix = None

        return super().__init__(name, bases, attrs)

    def __new__(meta, name, bases, dct):
        # only for subclasses, not for Cell class
        if bases:
            for k, v in dct.items():
                if (not k.startswith('_')
                        and inspect.isfunction(v)
                        and not hasattr(v, '_view')
                        and len(inspect.signature(v).parameters) == 1):
                    # turn functions with single argument (self) into cached properties
                    dct[k] = cached_property(v)

        return super().__new__(meta, name, bases, dct)


class Cell(metaclass=CellMeta):
    """
    View model base class which is basically a wrapper around a template.
    Templates can access attributes of the cell and some selected model properties directly.
    """
    model: ClassVar[Any]
    model_properties: Iterable[str] = []
    layout = True
    template_prefix: ClassVar[str]
    #: class that should be used to mark safe HTML output. Must be a subclass of str.
    markup_class: Type[str] = Markup

    def __init__(self,
                 model,
                 request: Request,
                 collection: Iterable=None,
                 layout: bool=None,
                 parent: Cell=None,
                 template_path: str=None,
                 **options) -> None:
        """
        """
        self._model = model
        self._request = request
        self.current_user = request.current_user
        self._app = request.app
        self._s = request.app.settings
        self.parent = parent
        self.collection = collection
        self._template_path = template_path
        self.options = options
        # if no parent is set, the layout is enabled by default. This can be overriden by the `layout` arg
        if layout is not None:
            self.layout = layout
        elif parent is None:
            self.layout = True
        else:
            self.layout = False

    @property
    def template_path(self) -> str:
        if self._template_path is None:
            cell_name = self.__class__.__name__
            if not cell_name.endswith('Cell'):
                raise Exception('Cell name does not end with Cell, you must override template_path!')

            name = case_conversion.snakecase(cell_name[:-len('Cell')])

            if self.template_prefix is not None:
                self._template_path = f"{self.template_prefix}/{name}.j2.jade"
            else:
                self._template_path = f"{name}.j2.jade"

        return self._template_path

    def render_template(self, template_path) -> str:
        return self.markup_class(self._request.render_template(template_path, _cell=self))

    def show(self):
        return self.render_template(self.template_path)

    # template helpers

    def link(self, model, name='', *args, **kwargs) -> str:
        return self._request.link(model, name, *args, **kwargs)

    def class_link(self, model_class, variables: Dict[str, Any], name='', *args, **kwargs) -> str:
        return self._request.class_link(model_class, variables, name, *args, **kwargs)

    def cell(self, model, layout: bool=None, view_name='', **options) -> Cell:
        """Look up a cell by model and create an instance.
        The parent cell is set to self which also means that it will be rendered without layout by default.
        """
        cell_class = find_cell_by_model_instance(model)
        return cell_class(model, self._request, layout=layout, parent=self, **options)

    def render_cell(self,
                    model=None,
                    view_name: str=None,
                    collection: Iterable=None,
                    separator: str=None,
                    layout: bool=None,
                    **options) -> str:
        """Look up a cell by model and render it to HTML.
        The parent cell is set to self which also means that it will be rendered without layout by default.
        """
        view_method = view_name if view_name is not None else 'show'
        if collection is not None:
            if model is not None:
                raise ValueError("model and collection arguments cannot be used together!")

            parts = [getattr(self.cell(item, layout=layout, **options), view_method)() for item in collection]

            if separator is None:
                separator = "\n"

            return self.markup_class(separator.join(parts))

        else:
            return getattr(self.cell(model, layout=layout, **options), view_method)()

    @staticmethod
    def view(func):
        """Decorator for cell methods that can be used as alternative views.
        """
        func._view = True
        return func

    @cached_property
    def self_link(self) -> str:
        return self.link(self._model)

    # magic starts here...

    def __getattr__(self, name):
        if name in self.model_properties:
            return getattr(self._model, name)

        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'." \
                             " Is it from the model? Did you forget to add it to 'model_properties'?")

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError as e:
            # standard __getitem__ raises an KeyError, let's do the same
            raise KeyError(e.args[0])

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

