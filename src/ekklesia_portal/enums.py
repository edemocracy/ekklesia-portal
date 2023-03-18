"""A place for public enums"""

from enum import Enum, StrEnum


class ArgumentType(StrEnum):
    PRO = 'pro'
    CONTRA = 'contra'


class EkklesiaUserType(StrEnum):
    PLAIN_MEMBER = 'plain member'
    ELIGIBLE_MEMBER = 'eligible member'
    SYSTEM_USER = 'system user'
    DELETED = 'deleted user'
    GUEST = 'guest'


class Majority(StrEnum):
    SIMPLE = '1/2'
    TWO_THIRDS = '2/3'


class PropositionStatus(StrEnum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    CHANGING = 'changing'
    ABANDONED = 'abandoned'
    QUALIFIED = 'qualified'
    SCHEDULED = 'scheduled'
    VOTING = 'voting'
    FINISHED = 'finished'


class PropositionRelationType(StrEnum):
    REPLACES = 'replaces'
    MODIFIES = 'modifies'


class PropositionVisibility(StrEnum):
    PUBLIC = 'public'
    UNLISTED = 'unlisted'
    HIDDEN = 'hidden'


class SecretVoterStatus(StrEnum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    RETRACTED = 'retracted'


class SupporterStatus(StrEnum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    RETRACTED = 'retracted'


class VotingType(StrEnum):
    ONLINE = 'online'
    ASSEMBLY = 'assembly'
    BOARD = 'board'
    URN = 'urn'


class VotingStatus(StrEnum):
    PREPARING = 'preparing'  # voting has not been started yet
    VOTING = 'voting'  # ballots have been transferred to a voting module and voting is open
    FINISHED = 'finished'  # voting is closed, results have been fetched
    ABORTED = 'aborted'  # voting stopped by administration


class OpenSlidesVotingResult(StrEnum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    NOT_DECIDED = 'not decided'


class VotingSystem(StrEnum):
    RANGE_APPROVAL = 'range_approval'


class VoteByUser(StrEnum):
    UNSURE = 'unsure'
    ACCEPT = 'accept'
    DECLINE = 'decline'
    ABSTENTION = 'abstention'
