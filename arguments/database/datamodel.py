from sqlalchemy import Unicode, Integer, Text, desc, Boolean
from sqlalchemy.sql import select, func
from sqlalchemy.orm import object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import ARRAY

from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin

from arguments import db
from arguments.database import integer_pk, integer_fk, TimeStamp, rel, FK, C, Model, Table, bref


make_searchable(options={'regconfig': 'pg_catalog.german'})


class QuestionQuery(BaseQuery, SearchQueryMixin):
    pass


class UserGroup(Model):

    __tablename__ = "usergroup"

    id = integer_pk()
    name = C(Unicode)


user_to_usergroup = Table("user_to_usergroup", db.metadata,
                          integer_fk("user.id", name="user_id", primary_key=True),
                          integer_fk(UserGroup.id, name="group_id", primary_key=True))


class User(Model, UserMixin):

    __tablename__ = "user"

    id = integer_pk()
    login_name = C(Unicode, unique=True)
    display_name = C(Unicode, unique=True)

    groups = rel(UserGroup, secondary=user_to_usergroup, backref="users")

    def __repr__(self):
        return "User '{}'".format(self.login_name)


class EkklesiaUserInfo(Model):

    __tablename__ = "oauth_info"

    user_id = C(FK(User.id), primary_key=True)
    auid = C(Unicode, unique=True)
    user_type = C(Unicode)
    verified = C(Boolean)
    all_nested_group_ids = C(ARRAY(Integer))
    nested_group_ids = C(ARRAY(Integer))
    user = rel(User, backref=bref("ekklesia_info", uselist=False))


class OAuthToken(Model, OAuthConsumerMixin):
    
    __tablename__ = "oauth_token"

    user_id = C(FK(User.id), primary_key=True)
    user = rel(User, backref="oauth_token_list")


class Tag(Model):
    __tablename__ = 'tag'
    id = integer_pk()
    tag = C(Unicode)

    def __repr__(self):
        return "Tag '{}'".format(self.tag)


tag_to_question = Table("tag_to_question", db.metadata,
                        integer_fk("question.id", name="question_id", primary_key=True),
                        integer_fk(Tag.id, name="tag_id", primary_key=True))

UP = 1
DOWN = -1

class VoteMixin(object):

    @property
    def is_upvote(self):
        return self.value == UP

    @property
    def is_downvote(self):
        return self.value == DOWN


class QuestionVote(Model, VoteMixin):

    __tablename__ = "question_vote"

    question_id = integer_fk("question.id", primary_key=True)
    user_id = integer_fk(User.id, primary_key=True)
    value = C(Integer, default=1)

    user = rel(User, backref=bref("question_votes", lazy="dynamic"))
    question = rel("Question", backref=bref("votes", lazy="dynamic"))

    def __repr__(self):
        return "QuestionVote '{}' for '{}'".format(self.value, self.question_id)


class ArgumentVote(Model, VoteMixin):

    __tablename__ = "argument_vote"

    argument_id = integer_fk("argument.id", primary_key=True)
    user_id = integer_fk(User.id, primary_key=True)
    value = C(Integer)

    user = rel(User, backref=bref("argument_votes", lazy="dynamic"))
    argument = rel("Argument", backref=bref("votes", lazy="dynamic"))

    def __repr__(self):
        return "ArgumentVote '{}' for '{}'".format(self.value, self.argument_id)


class Argument(Model, TimeStamp):

    __tablename__ = 'argument'

    id = integer_pk()
    title = C(Unicode)
    abstract = C(Unicode)
    details = C(Text)
    url = C(Unicode)
    author_id = integer_fk(User.id)
    question_id = integer_fk("question.id")
    argument_type = C(Unicode)
    parent_id = integer_fk(id)

    author = rel(User)
    _counter_arguments = rel("Argument", lazy="dynamic", backref=bref("parent", remote_side=[id]))
    question = rel("Question", backref=bref("arguments", lazy="dynamic"))

    @property
    def counter_arguments(self):
        return self._counter_arguments.order_by(desc(Argument.score))

    @hybrid_property
    def score(self):
        return self.votes.with_entities(func.coalesce(func.sum(ArgumentVote.value), 0)).scalar()

    @score.expression
    def score_expr(cls):
        return (select([func.coalesce(func.sum(ArgumentVote.value), 0)])
                .where(ArgumentVote.argument_id == cls.id))


    def user_vote(self, user):
        return self.votes.filter_by(user_id=user.id).scalar()

    def __repr__(self):
        return "Argument '{}' for '{}'".format(self.url, self.question_id)


class Question(Model, TimeStamp):

    query_class = QuestionQuery
    __tablename__ = 'question'

    id = integer_pk()
    details = C(Text)
    title = C(Unicode)
    url = C(Unicode)

    search_vector = C(TSVectorType('details', 'title', 'url'))


    tags = rel(Tag, secondary=tag_to_question, backref="questions")

    @hybrid_property
    def score(self):
        return self.votes.count()

    @score.expression
    def score_expr(cls):
        return (select([func.count("*")])
                .where(QuestionVote.question_id == cls.id)
                .label("votes_count"))

    @hybrid_property
    def pro_arguments(self):
        return self.arguments.filter_by(argument_type=u"pro", parent=None).order_by(desc(Argument.score))

    @hybrid_property
    def contra_arguments(self):
        return self.arguments.filter_by(argument_type=u"con", parent=None).order_by(desc(Argument.score))

    def user_vote(self, user):
        return self.votes.filter_by(user_id=user.id).scalar()

    def __repr__(self):
        return "Question '{}'".format(self.url)


class QuestionAssociation(Model):
    __tablename__ = "question_to_question"

    left_id = integer_fk(Question.id, primary_key=True)
    right_id = integer_fk(Question.id, primary_key=True)

    association_type = C(Unicode)
    left = rel(Question, primaryjoin=Question.id == left_id, backref=bref("right_assocs", lazy="dynamic"))
    right = rel(Question, primaryjoin=Question.id == right_id, backref=bref("left_assocs", lazy="dynamic"))

    def __repr__(self):
        return "Question {} -> {} ({})".format(self.left_id, self.right_id, self.association_type)


def associated_questions(self, association):
    return (self.right_assocs.filter_by(association_type=association)
        .with_entities(Question).filter(Question.id == QuestionAssociation.right_id))

Question.associated_questions = associated_questions

