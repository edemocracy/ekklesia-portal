"""A place for public enums"""

from enum import Enum
from ekklesia_portal.helper.translation import _


class EkklesiaUserType(str, Enum):
    PLAIN_MEMBER = 'plain member'
    ELIGIBLE_MEMBER = 'eligible member'
    SYSTEM_USER = 'system user'
    DELETED = 'deleted user'
    GUEST = 'guest'


class PropositionStatus(str, Enum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    CHANGING = 'changing'
    ABANDONED = 'abandoned'
    QUALIFIED = 'qualified'
    PLANNED = 'planned'
    VOTING = 'voting'
    FINISHED = 'finished'


class SupporterStatus(str, Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    RETRACTED = 'retracted'


class VotingType(str, Enum):
    ONLINE = 'online'
    ASSEMBLY = 'assembly'
    BOARD = 'board'
    URN = 'urn'


class VotingStatus(str, Enum):
    PREPARING = 'preparing' # no target date set
    SCHEDULED = 'scheduled' # target date set, but voting has not started
    VOTING = 'voting' # ballots have been transferred to a voting module and voting is open
    FINISHED = 'finished' # voting is closed, results have been fetched
    ABORTED = 'aborted' # voting stopped by administration

# XXX: add Enum support to babel extractor

_('voting_status_preparing')
_('voting_status_scheduled')
_('voting_status_voting')
_('voting_status_finished')
_('voting_status_aborted')
