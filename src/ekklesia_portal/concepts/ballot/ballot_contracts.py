from colander import Length
from deform.widget import Select2Widget
from sqlalchemy.orm import object_session
from ekklesia_portal.helper.contract import Schema, Form, string_property, list_property, int_property, bool_property, select2_widget_or_hidden
from ekklesia_portal.helper.translation import _


class BallotSchema(Schema):
    name = string_property(title=_('name'), validator=Length(min=2, max=23), missing='')
    election = int_property(title=_('election_positions'), missing=0)
    area_id = int_property(title=_('subject_area'), missing=None)
    voting_id = int_property(title=('voting_phase'), missing=None)
    proposition_type_id = int_property(title=('proposition_type'), missing=None)


class BallotForm(Form):

    def __init__(self, request, action):
        super().__init__(BallotSchema(), request, action, buttons=("submit", ))


    def prepare_for_render(self, items_for_selects):
        widgets = {
            'area_id': Select2Widget(values=items_for_selects['area']),
            'voting_id': Select2Widget(values=items_for_selects['voting']),
            'proposition_type_id': Select2Widget(values=items_for_selects['proposition_type'])
        }
        self.set_widgets(widgets)
