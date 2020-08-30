from colander import Length
from deform import Button
from deform.widget import HiddenWidget, Select2Widget, TextAreaWidget
from ekklesia_common.contract import Form, Schema, enum_property, int_property, string_property
from ekklesia_common.translation import _

from ekklesia_portal.enums import VoteByUser


class PropositionNoteSchema(Schema):
    proposition_id = string_property(title=_('proposition_id'), missing=None)
    user_id = int_property(title=_('user_id'), missing=None)
    notes = string_property(title=_('notes'), validator=Length(min=0, max=2048), missing=None)
    vote = enum_property(VoteByUser, title=_('vote'), missing=VoteByUser.UNSURE)


class PropositionNoteForm(Form):

    def __init__(self, request, action):
        super().__init__(PropositionNoteSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        self.set_widgets({
            'proposition_id': HiddenWidget(),
            'user_id': HiddenWidget(),
            'notes': TextAreaWidget(rows=8, missing=None),
            'vote': Select2Widget(values=items_for_selects['vote'])
        })
