from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Proposition

from .propositions import Propositions


@App.concept('proposition')
def proposition_concept():
    return {'model_class': Proposition, 'collection_class': Propositions}
