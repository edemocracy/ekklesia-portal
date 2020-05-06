import colander
from colander import Length, OneOf
from deform.widget import TextAreaWidget, HiddenWidget, SelectWidget, Select2Widget
from ekklesia_common.translation import _
from ekklesia_portal.enums import PropositionStatus, PropositionVisibility
from ekklesia_common.contract import Schema, string_property, set_property, int_property, \
     enum_property, json_property, Form


def common_widgets(items_for_selects):
    return {
        'title': TextAreaWidget(rows=2),
        'abstract': TextAreaWidget(rows=4),
        'content': TextAreaWidget(rows=8),
        'motivation': TextAreaWidget(rows=8),
        'tags': Select2Widget(multiple=True, tags=True, values=items_for_selects['tags']),
        'relation_type': HiddenWidget(),
        'related_proposition_id': HiddenWidget()
    }


class PropositionNewSchema(Schema):
    area_id = int_property(title=_('subject_area'))
    title = string_property(title=_('title'), validator=Length(min=5, max=512))
    external_discussion_url = string_property(title=_('external_discussion_url'), validator=colander.url, missing='')
    abstract = string_property(title=_('abstract'), validator=Length(min=5, max=2048))
    content = string_property(title=_('content'), validator=Length(min=10, max=65536))
    motivation = string_property(title=_('motivation'), missing='')
    tags = set_property(title=_('tags'), missing=tuple())
    relation_type = string_property(validator=OneOf(['replaces', 'modifies']), missing=None)
    related_proposition_id = int_property(missing=None)


class PropositionEditSchema(PropositionNewSchema):
    voting_identifier = string_property(title=_('voting_identifier'), validator=Length(max=10), missing=None)
    status = enum_property(PropositionStatus, title=_('status'))
    visibility = enum_property(PropositionVisibility, title=_('visibility'))
    external_fields = json_property(title=_('external_fields'), missing={})


class PropositionNewDraftSchema(Schema):
    title = string_property(title=_('title'), validator=Length(min=5, max=512))
    content = string_property(title=_('content'), validator=Length(min=5, max=50000))
    document_id = int_property()
    section = string_property()
    abstract = string_property(title=_('abstract'), validator=Length(max=2000))
    motivation = string_property(title=_('motivation'), missing='', validator=Length(max=50000))
    editing_remarks = string_property(title=_('editing_remarks'), missing='', validator=Length(max=2000))
    tags = set_property(title=_('tags'), missing=tuple())


class PropositionNewForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionNewSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        self.set_widgets({
            'area_id': Select2Widget(values=items_for_selects['area']),
            **common_widgets(items_for_selects)})


class PropositionEditForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionEditSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        self.set_widgets({
            'area_id': HiddenWidget(),
            'status': SelectWidget(values=items_for_selects['status']),
            'visibility': SelectWidget(values=items_for_selects['visibility']),
            'external_fields': TextAreaWidget(rows=4),
            **common_widgets(items_for_selects)})


class PropositionNewDraftForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionNewDraftSchema(), request, action, buttons=("submit", ))

    def prepare_for_render(self, items_for_selects):
        common = common_widgets(items_for_selects)
        self.set_widgets({
            'document_id': HiddenWidget(),
            'section': HiddenWidget(),
            'editing_remarks': TextAreaWidget(rows=4),
            'title': common['title'],
            'abstract': common['abstract'],
            'content': common['content'],
            'motivation': common['motivation'],
            'tags': common['tags']})
