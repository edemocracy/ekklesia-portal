import datetime
import string

import factory
from ekklesia_common.database import Session
from ekklesia_common.ekklesia_auth import EkklesiaAuthData
from factory import Factory, RelatedFactory, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import RelatedFactoryList
from factory.fuzzy import FuzzyChoice, FuzzyDecimal, FuzzyInteger, FuzzyText
from mimesis_factory import MimesisField
from pytest_factoryboy import register

from ekklesia_portal.datamodel import (
    Argument, ArgumentRelation, Ballot, CustomizableText, Department, Document, Group, Page, Policy, Proposition,
    PropositionType, SubjectArea, Tag, User, UserLoginToken, VotingPhase, VotingPhaseType
)
from ekklesia_portal.enums import ArgumentType, EkklesiaUserType, Majority, PropositionStatus, VotingStatus, VotingSystem, VotingType


class SQLAFactory(SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'flush'


@register
class DepartmentFactory(SQLAFactory):

    class Meta:
        model = Department

    name = Sequence('department{}'.format)
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

    name = Sequence('subject_area{}'.format)
    department = SubFactory(DepartmentFactory)
    description = MimesisField('text', quantity=5)


@register
class GroupFactory(SQLAFactory):

    class Meta:
        model = Group

    name = Sequence('group{}'.format)


@register
class UserFactory(SQLAFactory):

    class Meta:
        model = User

    auth_type = 'system'
    name = Sequence('user{}'.format)


register(UserFactory, 'user_two')


@register
class UserLoginTokenFactory(SQLAFactory):

    class Meta:
        model = UserLoginToken

    token = MimesisField('uuid')


@register
class PolicyFactory(SQLAFactory):

    class Meta:
        model = Policy

    name = Sequence('policy{}'.format)
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

    name = Sequence('proposition_type{}'.format)
    abbreviation = Sequence('P{}T'.format)
    description = MimesisField('text', quantity=5)
    policy = SubFactory(PolicyFactory)


@register
class BallotFactory(SQLAFactory):

    class Meta:
        model = Ballot

    name = Sequence('ballot{}'.format)
    election = FuzzyChoice([0, 4, 8])
    voting_type = FuzzyChoice(list(VotingType))
    proposition_type = SubFactory(PropositionTypeFactory)
    area = SubFactory(SubjectAreaFactory)
    result = {}


@register
class TagFactory(SQLAFactory):

    class Meta:
        model = Tag

    name = Sequence('tag{}'.format)


@register
class PropositionFactory(SQLAFactory):

    class Meta:
        model = Proposition

    title = MimesisField('title')
    content = MimesisField('text', quantity=5)
    motivation = MimesisField('text', quantity=8)
    abstract = MimesisField('text', quantity=2)
    status = PropositionStatus.DRAFT
    ballot = SubFactory(BallotFactory)
    tags = RelatedFactoryList(TagFactory)


register(PropositionFactory, 'proposition_two')


@register
class ArgumentFactory(SQLAFactory):

    class Meta:
        model = Argument

    title = MimesisField('title')
    abstract = MimesisField('text', quantity=2)
    details = MimesisField('text', quantity=4)


@register
class ArgumentRelationFactory(SQLAFactory):

    class Meta:
        model = ArgumentRelation

    argument = SubFactory(ArgumentFactory)
    proposition = SubFactory(PropositionFactory)
    argument_type = FuzzyChoice(list(ArgumentType))


@register
class EkklesiaAuthDataFactory(Factory):

    class Meta:
        model = EkklesiaAuthData

    sub = MimesisField('uuid')
    roles = []
    eligible = FuzzyChoice([True, False])
    verified = FuzzyChoice([True, False])
    verified: bool
    preferred_username = MimesisField('username', template='l_d')


@register
class VotingPhaseTypeFactory(SQLAFactory):

    class Meta:
        model = VotingPhaseType

    abbreviation = Sequence('V{}P'.format)
    description = MimesisField('text', quantity=10)
    name = Sequence('voting_phase_type{}'.format)
    secret_voting_possible = FuzzyChoice([True, False])
    voting_type = FuzzyChoice(list(VotingType))


@register
class VotingPhaseFactory(SQLAFactory):

    class Meta:
        model = VotingPhase

    title = MimesisField('title')
    name = Sequence('voting_phase{}'.format)
    # when setting the target date, another status than PREPARING must be set!
    target = None
    status = VotingStatus.PREPARING
    secret = True
    description = MimesisField('text', quantity=10)
    department = SubFactory(DepartmentFactory)
    phase_type = SubFactory(VotingPhaseTypeFactory)


@register
class PageFactory(SQLAFactory):

    class Meta:
        model = Page

    name = Sequence('page{}'.format)
    lang = 'en'
    title = MimesisField('title')
    text = MimesisField('text')
    permissions = '{}'


@register
class CustomizableTextFactory(SQLAFactory):

    class Meta:
        model = CustomizableText

    name = Sequence('customizable_text{}'.format)
    lang = 'en'
    text = MimesisField('text')
    permissions = '{}'


@register
class DocumentFactory(SQLAFactory):

    class Meta:
        model = Document

    name = Sequence('document{}'.format)
    lang = 'en'
    area = SubFactory(SubjectAreaFactory)
    proposition_type = SubFactory(PropositionTypeFactory)
    text = MimesisField('text')
    description = MimesisField('text')
