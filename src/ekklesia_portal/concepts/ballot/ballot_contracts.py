import colander
from colander import Length
from deform import Button
from deform.widget import HiddenWidget, Select2Widget, TextAreaWidget
from ekklesia_common.contract import Form, Schema, enum_property, int_property, json_property, string_property
from ekklesia_common.translation import _
from ekklesia_portal.enums import VotingType


class BallotSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=2, max=23), missing='')
    election = int_property(title=_('election_positions'), missing=0)
    result = json_property(title=_('voting_result'), missing={})
    area_id = int_property(title=_('subject_area'))
    voting_id = int_property(title=_('voting_phase'), missing=None)
    proposition_type_id = int_property(title=_('proposition_type'), missing=None)
    voting_type = enum_property(VotingType, title=_('voting_type'), missing=None)


class BallotForm(Form):

    def __init__(self, request, action):
        super().__init__(BallotSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'result': TextAreaWidget(rows=4),
            'election': HiddenWidget(),
            'area_id': Select2Widget(values=items_for_selects['area']),
            'voting_id': Select2Widget(values=items_for_selects['voting']),
            'proposition_type_id': Select2Widget(values=items_for_selects['proposition_type']),
            'voting_type': Select2Widget(values=items_for_selects['voting_type']),
        }
        self.set_widgets(widgets)
