import colander
from colander import Length, OneOf
from deform.widget import TextAreaWidget, TextInputCSVWidget, HiddenWidget, Select2Widget
from ekklesia_common.translation import _
from ekklesia_portal.enums import PropositionStatus
from ekklesia_common.contract import Schema, string_property, set_property, int_property, enum_property, Form


class PropositionSchema(Schema):
    area_id = int_property(title=_('subject_area'), missing=None)
    title = string_property(title=_('title'), validator=Length(min=5, max=512))
    voting_identifier = string_property(title=_('voting_identifier'), validator=Length(max=10), missing=None)
    external_discussion_url = string_property(title=_('external_discussion_url'), validator=colander.url)
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=2048))
    content = string_property(title=_('content'), validator=Length(min=10, max=65536))
    motivation = string_property(title=_('motivation'), missing='')
    tags = set_property(title=_('tags'), missing=tuple())
    status = enum_property(PropositionStatus, title=_('status'), missing=None)
    relation_type = string_property(validator=OneOf(['replaces', 'modifies']), missing=None)
    related_proposition_id = int_property(missing=None)


class PropositionNewSchema(Schema):
    area_id = int_property(title=_('subject_area'), missing=None)
    title = string_property(title=_('title'), validator=Length(min=5, max=512))
    external_discussion_url = string_property(title=_('external_discussion_url'), validator=colander.url)
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=2048))
    content = string_property(title=_('content'), validator=Length(min=10, max=65536))
    motivation = string_property(title=_('motivation'), missing='')
    tags = set_property(title=_('tags'), missing=tuple())
    status = enum_property(PropositionStatus, title=_('status'))
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


class PropositionNewForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionNewSchema(), request, action, buttons=("submit", ))

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
