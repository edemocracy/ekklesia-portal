import datetime
import string
import factory
from factory import Factory, SubFactory, RelatedFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDecimal, FuzzyInteger
from mimesis_factory import MimesisField
from pytest_factoryboy import register
from ekklesia_portal.database import Session
from ekklesia_portal.enums import EkklesiaUserType, Majority, VotingType, VotingStatus, VotingSystem
from ekklesia_portal.ekklesia_auth import EkklesiaAuthData, EkklesiaAUIDData, EkklesiaProfileData, EkklesiaMembershipData
from ekklesia_portal.database.datamodel import Proposition, Argument, ArgumentRelation, User, Department, SubjectArea, \
    VotingPhase, VotingPhaseType, Ballot, Policy, PropositionType, Group


class SQLAFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'flush'


@register
class DepartmentFactory(SQLAFactory):
    class Meta:
        model = Department

    name = MimesisField('word')
    description = MimesisField('text', quantity=5)

    @factory.post_generation
    def add_subject_areas(self, create, extracted, **kwargs):
        # self can also be a dict if factory.build(dict) is used
        if isinstance(self, Department):
            for _ in range(2):
                SubjectAreaFactory(department=self)


@register
class SubjectAreaFactory(SQLAFactory):
    class Meta:
        model = SubjectArea

    name = MimesisField('word')
    department = SubFactory(DepartmentFactory)


@register
class GroupFactory(SQLAFactory):
    class Meta:
        model = Group

    name = MimesisField('word')


@register
class UserFactory(SQLAFactory):
    class Meta:
        model = User

    auth_type = 'system'
    name = MimesisField('username', template='l_d')


register(UserFactory, 'user_two')


@register
class PolicyFactory(SQLAFactory):
    class Meta:
        model = Policy

    name = MimesisField('word')
    description = MimesisField('text', quantity=5)
    majority = FuzzyChoice(list(Majority))
    proposition_expiration = FuzzyInteger(0, 10000)
    qualification_quorum = FuzzyDecimal(0, 1)
    qualification_minimum = FuzzyInteger(0, 1000)
    range_max = FuzzyInteger(6, 10)
    range_small_max = FuzzyInteger(3, 5)
    range_small_options = FuzzyInteger(1, 10)
    secret_minimum = FuzzyInteger(0, 1000)
    secret_quorum = FuzzyDecimal(0, 1)
    submitter_minimum = FuzzyInteger(0, 1000)
    voting_duration = FuzzyInteger(0, 10000)
    voting_system = FuzzyChoice(list(VotingSystem))


@register
class PropositionTypeFactory(SQLAFactory):
    class Meta:
        model = PropositionType

    name = MimesisField('word')
    abbreviation = FuzzyText(length=3, chars=string.ascii_uppercase)
    description = MimesisField('text', quantity=5)
    policy = SubFactory(PolicyFactory)


@register
class BallotFactory(SQLAFactory):
    class Meta:
        model = Ballot

    name = MimesisField('word')
    election = FuzzyChoice([0, 4, 8])
    voting_type = FuzzyChoice(list(VotingType))
    proposition_type = SubFactory(PropositionTypeFactory)


@register
class PropositionFactory(SQLAFactory):
    class Meta:
        model = Proposition

    title = MimesisField('title')
    content = MimesisField('text', quantity=5)
    motivation = MimesisField('text', quantity=8)
    abstract = MimesisField('text', quantity=2)
    ballot = SubFactory(BallotFactory)


register(PropositionFactory, 'proposition_two')


@register
class ArgumentFactory(SQLAFactory):
    class Meta:
        model = Argument


@register
class ArgumentRelationFactory(SQLAFactory):
    class Meta:
        model = ArgumentRelation


@register
class EkklesiaMembershipDataFactory(Factory):
    class Meta:
        model = EkklesiaMembershipData

    nested_groups = all_nested_groups = [1, 2, 3]
    type = FuzzyChoice(list(EkklesiaUserType))
    verified = FuzzyChoice([True, False])


@register
class EkklesiaProfileDataFactory(Factory):
    class Meta:
        model = EkklesiaProfileData

    username = MimesisField('username', template='l_d')
    profile = MimesisField('text', quantity=2)
    avatar = ''


@register
class EkklesiaAUIDDataFactory(Factory):
    class Meta:
        model = EkklesiaAUIDData

    auid = MimesisField('uuid')


@register
class EkklesiaAuthDataFactory(Factory):
    class Meta:
        model = EkklesiaAuthData

    membership = SubFactory(EkklesiaMembershipDataFactory)
    profile = SubFactory(EkklesiaProfileDataFactory)
    auid = SubFactory(EkklesiaAUIDDataFactory)
    token = FuzzyText(length=30, chars=string.ascii_letters + string.digits)


@register
class VotingPhaseTypeFactory(SQLAFactory):
    class Meta:
        model = VotingPhaseType

    name = MimesisField('word')
    abbreviation = MimesisField('word')
    secret_voting_possible = True
    voting_type = FuzzyChoice(list(VotingType))


@register
class VotingPhaseFactory(SQLAFactory):
    class Meta:
        model = VotingPhase

    title = MimesisField('title')
    name = MimesisField('word')
    # when setting the target date, another status than PREPARING must be set!
    target = None
    status = VotingStatus.PREPARING
    secret = True
    description = MimesisField('text', quantity=10)
    department = SubFactory(DepartmentFactory)
    phase_type = SubFactory(VotingPhaseTypeFactory)
