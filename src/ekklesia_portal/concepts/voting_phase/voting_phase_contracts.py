from colander import Length
from deform.widget import TextAreaWidget, TextInputCSVWidget
from ekklesia_portal.helper.contract import Schema, string_property, list_property, int_property, bool_property, date_property, Form
from ekklesia_portal.helper.translation import _


class VotingPhaseSchema(Schema):
    target = date_property(title=_('target'))
    title = string_property(title=_('title'), validator=Length(min=5, max=140), missing='')
    name = string_property(title=_('name'), validator=Length(min=2, max=23), missing='')
    secret = bool_property(title=_('secret_voting_possible'))
    description = string_property(title=_('description'), validator=Length(min=10, max=65536), missing='')
    ballots = list_property(title=_('ballots'), missing=[])
    department_id = int_property()
    phase_type_id = int_property()


class VotingPhaseForm(Form):

    def __init__(self, request, action):
        super().__init__(VotingPhaseSchema(), request, action, buttons=("submit", ))
        self.set_widgets({
            'title': TextAreaWidget(rows=2),
            'description': TextAreaWidget(rows=8),
            'ballots': TextInputCSVWidget()
        })
