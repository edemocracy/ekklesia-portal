from colander import Length, OneOf
from deform.widget import TextAreaWidget, TextInputCSVWidget, HiddenWidget, Select2Widget
from ekklesia_portal.helper.contract import Schema, string_property, set_property, int_property, Form
from ekklesia_portal.helper.translation import _


class PropositionSchema(Schema):
    area_id = int_property(title=_('subject_area'), missing=None)
    title = string_property(title=_('title'), validator=Length(min=5, max=512))
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=2048))
    content = string_property(title=_('content'), validator=Length(min=10, max=65536))
    motivation = string_property(title=_('motivation'), missing='')
    tags = set_property(title=_('tags'), missing=tuple())
    relation_type = string_property(validator=OneOf(['replaces', 'modifies']), missing=None)
    related_proposition_id = int_property(missing=None)


class PropositionForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        self.set_widgets({
            'title': TextAreaWidget(rows=2),
            'abstract': TextAreaWidget(rows=4),
            'content': TextAreaWidget(rows=8),
            'motivation': TextAreaWidget(rows=8),
            'tags': Select2Widget(multiple=True, tags=True, values=items_for_selects['tags']),
            'relation_type': HiddenWidget(),
            'related_proposition_id': HiddenWidget(),
            'area_id': Select2Widget(values=items_for_selects['area'])
        })
