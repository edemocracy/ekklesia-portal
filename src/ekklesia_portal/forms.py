from deform import Form
from deform.widget import TextAreaWidget, TextInputCSVWidget, SelectWidget
from ekklesia_portal.schema import PropositionSchema


class PropositionForm(Form):

    def __init__(self, action):
        super().__init__(PropositionSchema(), action, buttons=("submit", ))
        self.set_widgets({
            'title': TextAreaWidget(rows=2),
            'short': TextAreaWidget(rows=4),
            'content': TextAreaWidget(rows=8),
            'motivation': TextAreaWidget(rows=8),
            'tags': TextInputCSVWidget(),
            'relation_type': SelectWidget(values=(('', ''), ('modifies', 'modifies'), ('replaces', 'replaces'))),
        })
