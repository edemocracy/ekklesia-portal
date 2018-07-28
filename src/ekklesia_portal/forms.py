from deform import Form
from deform.widget import TextAreaWidget, HiddenWidget
from ekklesia_portal.schema import ArgumentSchema, ArgumentForPropositionSchema


argument_widgets = {
    'abstract': TextAreaWidget(rows=2),
    'details': TextAreaWidget(rows=4)
}


class ArgumentForm(Form):

    def __init__(self, action):
        super().__init__(ArgumentSchema(), action, buttons=("submit", ))
        self.set_widgets(argument_widgets)


class ArgumentForPropositionForm(Form):

    def __init__(self, action):
        super().__init__(ArgumentForPropositionSchema(), action, buttons=("submit", ))
        self.set_widgets({
            'proposition_id': HiddenWidget(),
            'relation_type': HiddenWidget(),
            **argument_widgets
        })
