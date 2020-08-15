from colander import Length
from deform.widget import TextAreaWidget
from deform import Button
from ekklesia_common.contract import Form, Schema, string_property
from ekklesia_common.translation import _


class PageSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=3, max=255))
    lang = string_property(title=_('lang'), validator=Length(min=2, max=16))
    title = string_property(title=_('title'), validator=Length(max=255), missing='')
    text = string_property(title=_('text'), missing='')
    permissions = string_property(title=_('permissions'), missing='{}')


class PageForm(Form):

    def __init__(self, request, action):
        super().__init__(PageSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self):
        widgets = {'text': TextAreaWidget(rows=12)}
        self.set_widgets(widgets)
