from functools import wraps
import inspect
import dectate
from dectate import directive
from eliot import start_action
import morepath


class ConceptAction(dectate.Action):
    config = {
        'concepts': dict
    }

    def __init__(self, name):
        self.name = name

    def identifier(self, **_kw):
        return self.name

    def perform(self, obj, concepts):
        concepts[self.name] = obj


class ConceptApp(morepath.App):

    concept = directive(ConceptAction)

    @classmethod
    def html(cls, model, render=None, template=None, load=None,
                 permission=None, internal=False, **predicates):

        sup = super().html(model, render, template, load, permission, internal, **predicates)

        def add_log_wrapper(fn):
            argspec = inspect.getargspec(fn)
            num_args = len(argspec.args)
            arg_names = argspec.args
            fn_path = fn.__module__.split('.')

            if fn_path[1] == 'concepts':
                ctx = {
                    'app': fn_path[0],
                    'concept': fn_path[2].capitalize(),
                    'view': fn.__qualname__
                }
            else:
                ctx = {
                    'module': fn.__module__,
                    'view': fn.__qualname__
                }

            @wraps(fn)
            def log_wrapper(*args, **kwargs):

                model = args[0]
                model_data = model.to_dict() if hasattr(model, 'to_dict') else model

                ctx['model'] = model_data

                with start_action(action_type='html_view', **ctx):
                    return fn(*args, **kwargs)

            return sup(log_wrapper)

        return add_log_wrapper
