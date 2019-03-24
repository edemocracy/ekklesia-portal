from colander import Length
from deform.widget import TextAreaWidget
from ekklesia_portal.helper.contract import Schema, Form, string_property
from ekklesia_portal.helper.translation import _


class DepartmentSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=3, max=255))
    description = string_property(title=_('description'), validator=Length(min=10, max=2000), missing='')


class DepartmentForm(Form):

    def __init__(self, request, action):
        super().__init__(DepartmentSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self):
        widgets = {
            'description': TextAreaWidget(rows=8)
        }
        self.set_widgets(widgets)
