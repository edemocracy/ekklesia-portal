import dectate
from dectate import directive
import morepath


class ConceptAction(dectate.Action):
    config = {
        'concepts': dict
    }

    def __init__(self, name):
        self.name = name

    def identifier(self, **_kw):
        return self.name

    def perform(self, obj, concepts):
        concepts[self.name] = obj


class ConceptApp(morepath.App):

    concept = directive(ConceptAction)
