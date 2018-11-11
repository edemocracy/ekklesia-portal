from enum import Enum
from colander import SchemaNode, MappingSchema, SequenceSchema
from ekklesia_portal.helper.contract import bool_property, datetime_property, enum_property, int_property, list_property, string_property


class Auth(str, Enum):
    OAUTH = 'oAuth2'
    SHARED_PASSWORD = 'sharedPassw'


class Tally(str, Enum):
    CONFIGURABLE = 'configurableTally'


class SchemeName(str, Enum):
    YES_NO = 'yesNo'
    SCORE = 'score'


class SchemeMode(str, Enum):
    QUORUM = 'quorum'


class AuthData(MappingSchema):
    pass


class OAuthConfig(AuthData):
    RegistrationEndDate = datetime_property()
    RegistrationStartDate = datetime_property()
    eligible = bool_property()
    listId = string_property()
    nested_groups = list_property()
    serverId = string_property()
    verified = bool_property()


class Scheme(MappingSchema):
    name = enum_property(SchemeName)


class YesNoScheme(Scheme):
    abstention = bool_property()
    abstentionAsNo = bool_property()
    mode = enum_property(SchemeMode)
    quorum = int_property()


class ScoreScheme(Scheme):
    minScore = int_property()
    maxScore = int_property()


class Option(MappingSchema):
    optionID = int_property()
    proponents = list_property(missing=None)
    optionTitle = string_property()
    optionDesc = string_property()
    reasons = string_property(missing=None)


class Options(SequenceSchema):
    option = Option()


class Question(MappingSchema):
    questionID = int_property()
    questionWording = string_property()
    scheme = Scheme()
    findWinner = list_property()
    options = Options()


class Questions(SequenceSchema):
    question = Question()


class ElectionConfig(MappingSchema):
    auth = enum_property(Auth)
    authData = OAuthConfig()
    electionId = string_property()
    questions = Questions()
    tally = string_property()


