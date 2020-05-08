from colander import SchemaNode, Mapping, SequenceSchema, Int, Boolean, OneOf, Tuple
from deform import Button
from deform.widget import RadioChoiceWidget
from ekklesia_common.contract import Schema, Form
from ekklesia_common.translation import _


def ballot_voting_form(ballot_voting, request):

    yes_no_choices = [(True, _('Yes')), (False, _('No')), (None, _('Abstention'))]
    max_points = 9 if len(ballot_voting.options) > 3 else 3
    point_choices = [(i, str(i)) for i in range(max_points+1)]

    schema = Schema()

    for option in ballot_voting.options:

        option_schema = SchemaNode(Mapping(), name=str(option.uuid), title=option.title)

        option_schema.add(SchemaNode(
            Boolean(),
            validator=OneOf([x[0] for x in yes_no_choices]),
            widget=RadioChoiceWidget(values=yes_no_choices, inline=True),
            name='yes_no',
            title=f'Stimmst du dem Antrag zu?'))

        option_schema.add(SchemaNode(
            Int(),
            validator=OneOf([x[0] for x in point_choices]),
            widget=RadioChoiceWidget(values=point_choices, inline=True, null_value='0'),
            name='points',
            title='Welche Punktzahl gibst du dem Antrag?',
            missing=0))

        schema.add(option_schema)

    form = Form(schema, request, buttons=[Button(title=_('check'))])
    return form


def validate_form(form):
    pass
