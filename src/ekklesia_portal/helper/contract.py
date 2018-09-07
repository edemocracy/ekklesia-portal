from colander import SchemaNode, MappingSchema, \
    Int, String, Boolean, List, Date, DateTime
import deform
from more.babel_i18n.domain import Domain
from pkg_resources import resource_filename
from ekklesia_portal.request import Request


def string_property(**kwargs):
    return SchemaNode(String(), **kwargs)


def int_property(**kwargs):
    return SchemaNode(Int(), **kwargs)


def bool_property(**kwargs):
    return SchemaNode(Boolean(), **kwargs)


def list_property(**kwargs):
    return SchemaNode(List(), **kwargs)


def date_property(**kwargs):
    return SchemaNode(Date(), **kwargs)


def datetime_property(**kwargs):
    return SchemaNode(DateTime(), **kwargs)


class Schema(MappingSchema):
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
