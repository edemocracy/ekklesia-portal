from colander import Length
from deform import Button
from deform.widget import Select2Widget, TextAreaWidget
from ekklesia_common.contract import Form, Schema, int_property, string_property
from ekklesia_common.translation import _


class PropositionTypeSchema(Schema):
    name = string_property(title=_('name'), validator=Length(max=64))
    abbreviation = string_property(title=_('abbreviation'), validator=Length(max=6))
    description = string_property(title=_('description'), validator=Length(min=10, max=4000), missing='')
    policy_id = int_property(title=_('policy'))


class PropositionTypeForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionTypeSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'description': TextAreaWidget(rows=8),
            'policy_id': Select2Widget(values=items_for_selects['policy'])
        }
        self.set_widgets(widgets)
