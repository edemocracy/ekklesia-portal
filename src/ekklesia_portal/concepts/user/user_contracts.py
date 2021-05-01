from colander import Length
from deform import Button
from deform.widget import Select2Widget
from ekklesia_common.contract import Form, Schema, bool_property, set_property, string_property
from ekklesia_common.translation import _


class UserSchema(Schema):
    name = string_property(title=_('name'), validator=Length(max=128))
    email = string_property(title=_('email'), missing=None)
    active = bool_property(title=_('active'))
    groups = set_property(title=_('groups'), missing=tuple())


class UserForm(Form):

    def __init__(self, request, action):
        super().__init__(UserSchema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
            'groups': Select2Widget(multiple=True, values=items_for_selects['groups']),
        }
        self.set_widgets(widgets)
