"""A place for public enums"""

from enum import Enum


class EkklesiaUserType(str, Enum):
    PLAIN_MEMBER = 'plain member'
    ELIGIBLE_MEMBER = 'eligible member'
    SYSTEM_USER = 'system user'
    DELETED = 'deleted user'
    GUEST = 'guest'
