from sqlalchemy import Unicode, Integer, Text, desc
from sqlalchemy.sql import select, func
from sqlalchemy.orm import object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from arguments import db
from arguments.database import integer_pk, integer_fk, TimeStamp, rel, FK, C, Model, Table, bref


class UserGroup(Model):

    __tablename__ = "usergroup"

    id = integer_pk()
    name = C(Unicode)


user_to_usergroup = Table("user_to_usergroup", db.metadata,
                          integer_fk("user.id", name="user_id", primary_key=True),
                          integer_fk(UserGroup.id, name="group_id", primary_key=True))


class User(Model):

    __tablename__ = "user"

    id = integer_pk()
    login_name = C(Unicode, unique=True)

    groups = rel(UserGroup, secondary=user_to_usergroup, backref="users")


class Tag(Model):
    __tablename__ = 'tag'

    id = integer_pk()
    tag = C(Unicode)


tag_to_question = Table("tag_to_question", db.metadata,
                        integer_fk("question.id", name="question_id", primary_key=True),
                        integer_fk(Tag.id, name="tag_id", primary_key=True))

UP = 1
DOWN = -1

class VoteMixin(object):

    @property
    def is_upvote(self):
        return self.vote == UP

    @property
    def is_downvote(self):
        return self.vote == DOWN


class QuestionVote(Model, VoteMixin):

    __tablename__ = "question_vote"

    question_id = integer_fk("question.id", primary_key=True)
    user_id = integer_fk(User.id, primary_key=True)
    vote = C(Integer, default=1)

    user = rel(User, backref=bref("question_votes", lazy="dynamic"))
    question = rel("Question", backref=bref("votes", lazy="dynamic"))


class ArgumentVote(Model, VoteMixin):

    __tablename__ = "argument_vote"

    argument_id = integer_fk("argument.id", primary_key=True)
    user_id = integer_fk(User.id, primary_key=True)
    vote = C(Integer)

    user = rel(User, backref=bref("argument_votes", lazy="dynamic"))
    argument = rel("Argument", backref=bref("votes", lazy="dynamic"))


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
        return self.votes.with_entities(func.coalesce(func.sum(ArgumentVote.vote), 0)).scalar()

    @score.expression
    def score_expr(cls):
        return (select([func.coalesce(func.sum(ArgumentVote.vote), 0)])
                .where(ArgumentVote.argument_id == cls.id))


    def user_vote(self, user):
        return self.votes.filter_by(user_id=user.id).scalar()


class Question(Model, TimeStamp):

    __tablename__ = 'question'

    id = integer_pk()
    details = C(Text)
    title = C(Unicode)
    url = C(Unicode)

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


