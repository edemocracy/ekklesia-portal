# some view / cell helper that could be used from another concept
from ekklesia_common.translation import _

from ekklesia_portal.enums import VoteByUser


def items_for_proposition_note_select_widgets(model):
    return {'vote': [(name, _('vote_by_user_' + name.lower())) for name, member in VoteByUser.__members__.items()]}
