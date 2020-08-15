from colander import Length
from deform import Form
from deform.widget import TextAreaWidget, TextInputWidget
from ekklesia_common.contract import Schema, string_property
from ekklesia_common.translation import _

TITLE_MAXLENGTH = 80
ABSTRACT_MAXLENGTH = 160


class ArgumentSchema(Schema):
    title = string_property(title=_('title'), validator=Length(min=5, max=TITLE_MAXLENGTH))
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=ABSTRACT_MAXLENGTH))
    details = string_property(title=_('details'), validator=Length(min=10, max=4096), missing='')


argument_widgets = {
    'title': TextInputWidget(attributes={'maxlength': TITLE_MAXLENGTH}),
    'abstract': TextAreaWidget(rows=2, attributes={'maxlength': ABSTRACT_MAXLENGTH}),
    'details': TextAreaWidget(rows=4)
}


class ArgumentForm(Form):

    def __init__(self, request, action):
        super().__init__(ArgumentSchema(), request, action, buttons=[Button(title=_("submit"))])
        self.set_widgets(argument_widgets)
