from colander import Length
from deform.widget import TextAreaWidget, Select2Widget
from ekklesia_portal.helper.contract import Schema, Form, int_property, string_property
from ekklesia_portal.helper.translation import _


class PropositionTypeSchema(Schema):
    name = string_property(title=_('name'), validator=Length(max=64))
    description = string_property(title=_('name'), validator=Length(min=10, max=4000), missing='')
    policy_id = int_property(title=_('policy'))


class PropositionTypeForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionTypeSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'description': TextAreaWidget(rows=8),
            'policy_id': Select2Widget(values=items_for_selects['policy'])
        }
        self.set_widgets(widgets)
