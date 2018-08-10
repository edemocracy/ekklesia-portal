from colander import Length, OneOf
from deform.widget import TextAreaWidget, TextInputCSVWidget, SelectWidget
from ekklesia_portal.helper.contract import Schema, string_property, list_property, int_property, Form


class PropositionSchema(Schema):
    title = string_property(validator=Length(min=5, max=512))
    abstract = string_property(validator=Length(min=5, max=2048))
    content = string_property(validator=Length(min=10, max=65536))
    motivation = string_property(missing='')
    tags = list_property(missing=tuple())
    relation_type = string_property(validator=OneOf(['replaces', 'modifies']), missing=None)
    related_proposition_id = int_property(missing=None)


class PropositionForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionSchema(), request, action, buttons=("submit", ))
        self.set_widgets({
            'title': TextAreaWidget(rows=2),
            'abstract': TextAreaWidget(rows=4),
            'content': TextAreaWidget(rows=8),
            'motivation': TextAreaWidget(rows=8),
            'tags': TextInputCSVWidget(),
            'relation_type': SelectWidget(values=(('', ''), ('modifies', 'modifies'), ('replaces', 'replaces'))),
        })
