from colander import Length
from deform import Button
from deform.widget import SelectWidget, TextAreaWidget
from ekklesia_common.contract import Schema, Form, int_property, string_property
from ekklesia_common.translation import _


class SubjectAreaSchema(Schema):
    name = string_property(title=_('name'), validator=Length(max=255))
    department_id = int_property(title=_('department'))
    description = string_property(title=_('description'), validator=Length(max=2000), missing='')


class SubjectAreaForm(Form):

    def __init__(self, request, action):
        super().__init__(SubjectAreaSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'department_id': SelectWidget(values=items_for_selects['department']),
            'description': TextAreaWidget(rows=8),
        }
        self.set_widgets(widgets)
