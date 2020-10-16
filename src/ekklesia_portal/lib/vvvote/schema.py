from datetime import datetime
from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import List, Optional, Union

from dataclasses_json import dataclass_json
import dataclasses_json
import marshmallow

def iso_date_field():
    return dataclasses.field(
    metadata=dataclasses_json.config(
        encoder=datetime.isoformat,
        decoder=datetime.fromisoformat,
        mm_field=marshmallow.fields.DateTime(format='iso'),
    )
)


class Auth(str, Enum):
    OAUTH = 'oAuth2'
    SHARED_PASSWORD = 'sharedPassw'  # nosec


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
    RegistrationEndDate: datetime = iso_date_field()
    RegistrationStartDate: datetime = iso_date_field()
    VotingStart: datetime = iso_date_field()
    VotingEnd: datetime = iso_date_field()


@dataclass_json
@dataclass
class OAuthConfig(AuthData):
    serverId: str
    nested_groups: List[str]
    eligible: bool
    verified: bool
    external_voting: bool
    listId: str = ""


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
    electionTitle: str
    questions: List[Question]
    tally: Tally

    def __post_init__(self):
        if not isinstance(self.tally, Tally):
            self.tally = Tally(self.tally)

        if not isinstance(self.auth, Auth):
            self.auth = Auth(self.auth)
