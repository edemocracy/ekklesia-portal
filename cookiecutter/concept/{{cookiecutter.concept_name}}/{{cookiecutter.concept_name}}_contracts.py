#from colander import Length
from deform import Button
#from deform.widget import TextAreaWidget, Select2Widget
#from {{ cookiecutter.app_name }}.enums import {{ cookiecutter.ConceptName }}Status
from ekklesia_common.contract import Schema, Form  #, string_property, enum_property
from ekklesia_common.translation import _


class {{ cookiecutter.ConceptName }}Schema(Schema):
    pass
    # some field examples
    #name = string_property(title=_('name'), validator=Length(min=3, max=255))
    #description = string_property(title=_('name'), validator=Length(min=10, max=2000), missing='')
    #status = enum_property({{ cookiecutter.ConceptName }}Status, title=_('{{ cookiecutter.concept_name }}status'))
    #tags = set_property(title=_('tags'), missing=tuple())


class {{ cookiecutter.ConceptName }}Form(Form):

    def __init__(self, request, action):
        super().__init__({{ cookiecutter.ConceptName }}Schema(), request, action, buttons=[Button(title=_("submit"))])

    def prepare_for_render(self, items_for_selects):
        widgets = {
    #        'description': TextAreaWidget(rows=8),
    #        'status': Select2Widget(values=items_for_selects['{{ cookiecutter.concept_name }}_status']),
    #        'tags': Select2Widget(multiple=True, tags=True, values=items_for_selects['tags']),
        }
        self.set_widgets(widgets)
