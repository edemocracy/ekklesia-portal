import colander
import deform
from deform.widget import Select2Widget, HiddenWidget
from more.babel_i18n.domain import Domain
from pkg_resources import resource_filename
from ekklesia_portal.request import Request


def string_property(**kwargs):
    return colander.SchemaNode(colander.String(), **kwargs)


def int_property(**kwargs):
    return colander.SchemaNode(colander.Int(), **kwargs)


def bool_property(**kwargs):
    return colander.SchemaNode(colander.Boolean(), **kwargs)


def list_property(**kwargs):
    return colander.SchemaNode(colander.List(), **kwargs)


def set_property(**kwargs):
    return colander.SchemaNode(colander.Set(), **kwargs)


def date_property(**kwargs):
    return colander.SchemaNode(colander.Date(), **kwargs)


def enum_property(enum_cls, **kwargs):
    return colander.SchemaNode(colander.Enum(enum_cls), **kwargs)


def datetime_property(**kwargs):
    return colander.SchemaNode(colander.DateTime(), **kwargs)


class Schema(colander.MappingSchema):
    pass


COLANDER_TRANSLATION_DIR = resource_filename('colander', 'locale/')
DEFORM_TRANSLATION_DIR = resource_filename('deform', 'locale/')
EKKLESIA_PORTAL_TRANSLATION_DIR = resource_filename('ekklesia_portal', 'translations/')
DEFORM_TEMPLATE_DIRS = [resource_filename('deform', 'templates/')]


class Form(deform.Form):
    """
    Deform Form with more.babel_i18n integration.
    """

    def __init__(self, schema: Schema, request: Request, *args, **kwargs) -> None:

        # Domain depends on request, so it must be created here
        domains = {
            'colander': Domain(request=request, dirname=COLANDER_TRANSLATION_DIR, domain='colander'),
            'deform': Domain(request=request, dirname=DEFORM_TRANSLATION_DIR, domain='deform'),
            'messages': Domain(request=request, dirname=EKKLESIA_PORTAL_TRANSLATION_DIR, domain='messages')
        }

        def translator(term):
            domain = domains.get(term.domain)
            if domain is None:
                return term
            return domain.gettext(term)

        renderer = deform.ZPTRendererFactory(
            DEFORM_TEMPLATE_DIRS,
            translator=translator
        )
        super().__init__(schema, *args, renderer=renderer, **kwargs)


def select2_widget_or_hidden(values):
    """ Render a select2 widget or a hidden field if no values were given.
    XXX: Is there a better way to hide unwanted fields?
    """
    if values is None:
        return HiddenWidget(hidden=True)
    else:
        return Select2Widget(values=values)

