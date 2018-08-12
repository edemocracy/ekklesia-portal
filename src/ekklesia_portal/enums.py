"""A place for public enums"""

from enum import Enum


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
