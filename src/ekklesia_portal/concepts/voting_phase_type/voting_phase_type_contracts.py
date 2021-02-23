from colander import Length
from deform import Button
from deform.widget import Select2Widget, TextAreaWidget
from ekklesia_common.contract import Schema, Form, bool_property, string_property, enum_property
from ekklesia_common.translation import _

from ekklesia_portal.enums import VotingType


class VotingPhaseTypeSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=3, max=255))
    abbreviation = string_property(title=_('abbreviation'), validator=Length(max=3))
    secret_voting_possible = bool_property(title=_('secret_voting_possible'))
    voting_type = enum_property(VotingType, title=_('voting_type'))
    description = string_property(title=_('description'), validator=Length(min=10, max=2000), missing='')


class VotingPhaseTypeForm(Form):

    def __init__(self, request, action):
        super().__init__(VotingPhaseTypeSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'voting_type': Select2Widget(values=items_for_selects['voting_type']),
            'description': TextAreaWidget(rows=8),
        }
        self.set_widgets(widgets)
