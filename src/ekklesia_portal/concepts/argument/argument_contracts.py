from colander import Length
from deform import Form
from deform.widget import TextAreaWidget
from ekklesia_portal.helper.contract import Schema, string_property


class ArgumentSchema(Schema):
    title = string_property(validator=Length(min=5, max=80))
    abstract = string_property(validator=Length(min=5, max=140))
    details = string_property(validator=Length(min=10, max=4096), missing='')


argument_widgets = {
    'abstract': TextAreaWidget(rows=2),
    'details': TextAreaWidget(rows=4)
}


class ArgumentForm(Form):

    def __init__(self, request, action):
        super().__init__(ArgumentSchema(), request, action, renderer=renderer, buttons=("submit", ))
        self.set_widgets(argument_widgets)
