from colander import Length
from deform import Button
from deform.widget import SelectWidget, TextAreaWidget
from ekklesia_common.contract import Form, Schema, int_property, string_property
from ekklesia_common.translation import _


class DocumentSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=3, max=60))
    lang = string_property(title=_('lang'), validator=Length(min=2, max=16))
    area_id = int_property(title=_('subject_area'))
    proposition_type_id = int_property(title=('proposition_type'))
    description = string_property(title=_('description'), validator=Length(min=10, max=2000), missing='')
    text = string_property(title=_('text'), validator=Length(min=10), missing='')


class DocumentForm(Form):

    def __init__(self, request, action):
        super().__init__(DocumentSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'area_id': SelectWidget(values=items_for_selects['area']),
            'proposition_type_id': SelectWidget(values=items_for_selects['proposition_type']),
            'description': TextAreaWidget(rows=8),
            'text': TextAreaWidget(rows=20)
        }
        self.set_widgets(widgets)
