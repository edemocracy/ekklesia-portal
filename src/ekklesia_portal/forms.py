from deform import Form
from deform.widget import TextAreaWidget, TextInputCSVWidget, SelectWidget, HiddenWidget
from ekklesia_portal.schema import PropositionSchema, ArgumentSchema, ArgumentForPropositionSchema


class PropositionForm(Form):

    def __init__(self, action):
        super().__init__(PropositionSchema(), action, buttons=("submit", ))
        self.set_widgets({
            'title': TextAreaWidget(rows=2),
            'abstract': TextAreaWidget(rows=4),
            'content': TextAreaWidget(rows=8),
            'motivation': TextAreaWidget(rows=8),
            'tags': TextInputCSVWidget(),
            'relation_type': SelectWidget(values=(('', ''), ('modifies', 'modifies'), ('replaces', 'replaces'))),
        })


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
