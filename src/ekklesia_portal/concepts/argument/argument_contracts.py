from colander import Length
from deform import Form
from deform.widget import TextAreaWidget
from ekklesia_portal.helper.contract import Schema, string_property
from ekklesia_portal.helper.translation import _


class ArgumentSchema(Schema):
    title = string_property(title=_('title'), validator=Length(min=5, max=80))
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=140))
    details = string_property(title=_('details'), validator=Length(min=10, max=4096), missing='')


argument_widgets = {
    'abstract': TextAreaWidget(rows=2),
    'details': TextAreaWidget(rows=4)
}


class ArgumentForm(Form):

    def __init__(self, request, action):
        super().__init__(ArgumentSchema(), request, action, buttons=("submit", ))
        self.set_widgets(argument_widgets)
