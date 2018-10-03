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


class BallotForm(Form):

    def __init__(self, request, action=None, items_for_select_widgets={}):
        super().__init__(BallotSchema(), request, action, buttons=("submit", ))

        if items_for_select_widgets:
            widgets = {
                'area_id': Select2Widget(values=items_for_select_widgets['area']),
                'voting_id': Select2Widget(values=items_for_select_widgets['voting'])
            }
            self.set_widgets(widgets)
