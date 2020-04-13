from colander import Length
from deform.widget import TextAreaWidget
from ekklesia_common.contract import Schema, Form, json_property, string_property
from ekklesia_common.translation import _


class DepartmentSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=3, max=255))
    description = string_property(title=_('description'), validator=Length(min=10, max=2000), missing='')
    exporter_settings = json_property(title=_('exporter_settings'), missing={})


class DepartmentForm(Form):

    def __init__(self, request, action):
        super().__init__(DepartmentSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self):
        widgets = {
            'description': TextAreaWidget(rows=8),
            'exporter_settings': TextAreaWidget(rows=6)
        }
        self.set_widgets(widgets)
