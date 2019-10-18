from colander import Length
from deform.widget import TextAreaWidget, TextInputCSVWidget, SelectWidget
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.helper.contract import Schema, string_property, list_property, int_property, bool_property, date_property, enum_property, Form
from ekklesia_portal.helper.translation import _


class VotingPhaseSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=2, max=23), missing='')
    title = string_property(title=_('title'), validator=Length(min=5, max=140), missing='')
    target = date_property(title=_('target'), missing=None)
    status = enum_property(VotingStatus, title=_('voting_status'))
    department_id = int_property(title=_('department'))
    phase_type_id = int_property(title=_('voting_phase_type'))
    secret = bool_property(title=_('secret_voting_possible'))
    description = string_property(title=_('description'), validator=Length(min=10, max=65536), missing='')


class VotingPhaseForm(Form):

    def __init__(self, request, action):
        super().__init__(VotingPhaseSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'title': TextAreaWidget(rows=2),
            'description': TextAreaWidget(rows=8),
            'status': SelectWidget(values=items_for_selects['status']),
            'phase_type_id': SelectWidget(values=items_for_selects['phase_type']),
            'department_id': SelectWidget(values=items_for_selects['department'])
        }
        self.set_widgets(widgets)
