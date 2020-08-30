from deform import Button
from deform.widget import HiddenWidget
from ekklesia_common.contract import Form, enum_property, int_property, string_property
from ekklesia_common.translation import _

from ekklesia_portal.concepts.argument.argument_contracts import ArgumentSchema, argument_widgets
from ekklesia_portal.enums import ArgumentType


class ArgumentForPropositionSchema(ArgumentSchema):
    proposition_id = string_property()
    relation_type = enum_property(ArgumentType)


class ArgumentForPropositionForm(Form):

    def __init__(self, request, action):
        super().__init__(ArgumentForPropositionSchema(), request, action, buttons=[Button(title=_("submit"))])
        self.set_widgets({'proposition_id': HiddenWidget(), 'relation_type': HiddenWidget(), **argument_widgets})
