import datetime
import string
import factory
from factory import Factory, SubFactory, RelatedFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText
from mimesis_factory import MimesisField
from pytest_factoryboy import register
from ekklesia_portal.database import Session
from ekklesia_portal.enums import EkklesiaUserType, VotingType
from ekklesia_portal.ekklesia_auth import EkklesiaAuthData, EkklesiaAUIDData, EkklesiaProfileData, EkklesiaMembershipData
from ekklesia_portal.database.datamodel import Proposition, Argument, ArgumentRelation, User, Department, SubjectArea, VotingPhase, VotingPhaseType



class SQLAFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'flush'


@register
class SubjectAreaFactory(SQLAFactory):
    class Meta:
        model = SubjectArea

    name = MimesisField('word')


@register
class DepartmentFactory(SQLAFactory):
    class Meta:
        model = Department

    name = MimesisField('word')

    @factory.post_generation
    def add_subject_areas(self, create, extracted, **kwargs):
        for _ in range(2):
            self.areas.append(SubjectAreaFactory(department_id=self.id))


@register
class UserFactory(SQLAFactory):
    class Meta:
        model = User

    auth_type = 'system'
    name = MimesisField('username', template='l_d')


register(UserFactory, 'user_two')


class UserWithDepartmentsFactory(UserFactory):

    departments = factory.List([SubFactory(DepartmentFactory), SubFactory(DepartmentFactory)])

    @factory.post_generation
    def add_subject_areas(self, create, extracted, **kwargs):
        for department in self.departments:
            self.areas.extend(department.areas)


register(UserWithDepartmentsFactory, 'user_with_departments')


@register
class PropositionFactory(SQLAFactory):
    class Meta:
        model = Proposition

    title = MimesisField('title')
    content = MimesisField('text', quantity=100)
    abstract = MimesisField('text', quantity=20)


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
    target = datetime.date.today()
    secret = True
    description = MimesisField('text', quantity=10)
    department = SubFactory(DepartmentFactory)
    phase_type = SubFactory(VotingPhaseTypeFactory)
