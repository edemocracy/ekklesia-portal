from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
import datetime
from typing import List, Union, Optional


class Auth(str, Enum):
    OAUTH = 'oAuth2'
    SHARED_PASSWORD = 'sharedPassw'


class Tally(str, Enum):
    PUBLISH_ONLY = 'publishOnly'
    CONFIGURABLE = 'configurableTally'


class SchemeName(str, Enum):
    YES_NO = 'yesNo'
    SCORE = 'score'
    RANDOM = 'random'


class SchemeMode(str, Enum):
    QUORUM = 'quorum'


@dataclass_json
@dataclass
class AuthData:
    RegistrationEndDate: datetime.datetime
    RegistrationStartDate: datetime.datetime
    VotingStart: datetime.datetime
    VotingEnd: datetime.datetime

    def __post_init__(self):
        if isinstance(self.RegistrationStartDate, datetime.datetime):
            self.RegistrationStartDate = self.RegistrationStartDate.isoformat()

        if isinstance(self.RegistrationEndDate, datetime.datetime):
            self.RegistrationEndDate = self.RegistrationEndDate.isoformat()

        if isinstance(self.VotingStart, datetime.datetime):
            self.VotingStart = self.VotingStart.isoformat()

        if isinstance(self.VotingEnd, datetime.datetime):
            self.VotingEnd = self.VotingEnd.isoformat()


@dataclass_json
@dataclass
class OAuthConfig(AuthData):
    eligible: bool
    listId: str
    nested_groups: List[str]
    serverId: str
    verified: bool


@dataclass_json
@dataclass
class SharedPasswordConfig(AuthData):
    sharedPassw: str


@dataclass_json
@dataclass
class Scheme:
    name: SchemeName


@dataclass_json
@dataclass
class YesNoScheme(Scheme):
    abstention: bool
    abstentionAsNo: bool
    mode: SchemeMode
    quorum: int

    def __post_init__(self):
        if not isinstance(self.mode, SchemeMode):
            self.mode = SchemeMode(self.mode)


@dataclass_json
@dataclass
class ScoreScheme(Scheme):
    minScore: int
    maxScore: int


@dataclass_json
@dataclass
class Option:
    optionID: int
    proponents: List[str]
    optionTitle: str
    optionDesc: str
    reasons: Optional[str] = None


@dataclass_json
@dataclass
class Question:
    questionID: int
    questionWording: str
    options: List[Option]
    scheme: Optional[List[Scheme]] = None
    findWinner: Optional[List[SchemeName]] = None

    def __post_init__(self):
        if not self.findWinner:
            return

        if not isinstance(self.findWinner[0], SchemeName):
            self.findWinner = [SchemeName(name) for name in self.findWinner]


@dataclass_json
@dataclass
class ElectionConfig:
    auth: Auth
    authData: OAuthConfig
    electionId: str
    questions: List[Question]
    tally: Tally

    def __post_init__(self):
        if not isinstance(self.tally, Tally):
            self.tally = Tally(self.tally)

        if not isinstance(self.auth, Auth):
            self.auth = Auth(self.auth)
