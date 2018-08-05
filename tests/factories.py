from factory.alchemy import SQLAlchemyModelFactory
from mimesis_factory import MimesisField
from pytest_factoryboy import register
from ekklesia_portal.database import Session
from ekklesia_portal.database.datamodel import Proposition, Argument, ArgumentRelation, User


class SQLAFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session


@register
class UserFactory(SQLAFactory):
    class Meta:
        model = User

    auth_type = 'system'
    name = MimesisField('username', template='l_d')


register(UserFactory, 'user_two')

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
