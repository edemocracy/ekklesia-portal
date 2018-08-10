from colander import SchemaNode, MappingSchema, \
    Int, String, Boolean, List
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


class Schema(MappingSchema):
    pass


COLANDER_TRANSLATION_DIR = resource_filename('colander', 'locale/')
DEFORM_TRANSLATION_DIR = resource_filename('deform', 'locale/')
DEFORM_TEMPLATE_DIRS = [resource_filename('deform', 'templates/')]


class Form(deform.Form):
    """
    Deform Form with more.babel_i18n integration.
    """

    def __init__(self, schema: Schema, request: Request, *args, **kwargs) -> None:

        # Domain depends on request, so it must be created here
        colander_domain = Domain(request=request, dirname=COLANDER_TRANSLATION_DIR, domain='colander')
        deform_domain = Domain(request=request, dirname=DEFORM_TRANSLATION_DIR, domain='deform')

        def translator(term):
            translated = deform_domain.gettext(term)
            if translated != term:
                return translated
            # no translation happened, try again with other domain
            return colander_domain.gettext(term)

        renderer = deform.ZPTRendererFactory(
            DEFORM_TEMPLATE_DIRS,
            translator=translator
        )
        super().__init__(schema, *args, renderer=renderer, **kwargs)
