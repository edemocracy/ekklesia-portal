# some view / cell helper that could be used from another concept
from ekklesia_common.translation import _

from ekklesia_portal.enums import VoteByUser


def items_for_proposition_note_select_widgets(_model):

    vote = [(e.name, _('_'.join(['vote_by_user', e.value]))) for e in VoteByUser]

    return {'vote': vote}
