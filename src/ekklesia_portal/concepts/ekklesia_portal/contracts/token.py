from colander import OneOf
from deform import Button
from ekklesia_portal.helper.contract import Schema, bool_property, Form
from ekklesia_portal.helper.translation import _

class TokenSchema(Schema):
    tos_consent = bool_property(title=_('tos_consent'), validator=OneOf([True]))


class TokenForm(Form):

    def __init__(self, request, action):
        super().__init__(TokenSchema(), request, action, buttons=[Button(title=_("submit"))])
