from ekklesia_common.translation import _

from ekklesia_portal.enums import Majority, VotingSystem


def items_for_policy_select_widgets():
    majority_items = [(e.name, _('_'.join(['majority', e.value]))) for e in Majority]
    voting_system_items = [(e.name, _('_'.join(['majority', e.value]))) for e in VotingSystem]
    return {'majority': majority_items, 'voting_system': voting_system_items}
