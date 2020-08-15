from colander import Length
from deform import Button
from deform.widget import SelectWidget, TextAreaWidget
from ekklesia_common.contract import Form, Schema, decimal_property, enum_property, int_property, string_property
from ekklesia_common.translation import _

from ekklesia_portal.enums import Majority, VotingSystem


class PolicySchema(Schema):
    name = string_property(title=_('name'), validator=Length(max=64))
    description = string_property(title=_('description'), validator=Length(max=4000), missing='')
    majority = enum_property(Majority, title=_('majority'))
    proposition_expiration = int_property(title=_('proposition_expiration'))
    qualification_minimum = int_property(title=_('qualification_minimum'))
    qualification_quorum = decimal_property(title=_('qualification_quorum'))
    range_max = int_property(title=_('range_max'))
    range_small_max = int_property(title=_('range_small_max'))
    range_small_options = int_property(title=_('range_small_options'))
    secret_minimum = int_property(title=_('secret_minimum'))
    secret_quorum = decimal_property(title=_('secret_quorum'))
    submitter_minimum = int_property(title=_('submitter_minimum'))
    voting_duration = int_property(title=_('voting_duration'))
    voting_system = enum_property(VotingSystem, title=_('voting_system'))


class PolicyForm(Form):

    def __init__(self, request, action):
        super().__init__(PolicySchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'description': TextAreaWidget(rows=8),
            'majority': SelectWidget(values=items_for_selects['majority']),
            'voting_system': SelectWidget(values=items_for_selects['voting_system']),
        }
        self.set_widgets(widgets)
