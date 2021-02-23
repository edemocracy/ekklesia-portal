from ekklesia_common.translation import _

from ekklesia_portal.enums import VotingType


def items_for_voting_phase_type_select_widgets(model):
    voting_type_items = [(e.name, _('_'.join(['voting_type', e.value]))) for e in VotingType]
    return {'voting_type': voting_type_items}
