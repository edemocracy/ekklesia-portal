from sqlalchemy import Unicode, Integer, Text
from arguments import db
from arguments.database import integer_pk, integer_fk, TimeStamp, rel, FK, C, Model, Table


class User(Model):

    __tablename__ = "user"

    id = integer_pk()
    login_name = C(Unicode, unique=True)


class UserGroup(Model):

    __tablename__ = "usergroup"

    id = integer_pk()


user_to_usergroup = Table("user_to_usergroup", db.metadata,
        integer_fk(User.id, name="user_id", primary_key=True),
        integer_fk(UserGroup.id, name="group_id", primary_key=True))


class Argument(Model):

    __tablename__ = 'argument'

    id = integer_pk()
    headline = C(Unicode)
    abstract = C(Unicode)
    details = C(Text)
    url = C(Unicode)
    user_id = integer_fk(User.id)

    user = rel(User)


class Question(Model):
    
    __tablename__ = 'question'

    id = integer_pk()
    details = C(Text)
    title = C(Unicode)
    url = C(Unicode)


class Tag(Model):
    __tablename__ = 'tag'

    id = integer_pk()
    tag = C(Unicode)


tag_to_question = Table("tag_to_question", db.metadata,
    integer_fk(Question.id, name="question_id", primary_key=True),
    integer_fk(Tag.id, name="tag_id", primary_key=True))


class Vote(Model, TimeStamp):
    __tablename__ = 'vote'

    argument_id = integer_fk(Argument.id, primary_key=True)
    question_id = integer_fk(Question.id, primary_key=True)
    user_id = integer_fk(User.id)

    user = rel(User)
    question = rel(Question)
    arguments = rel(Argument)
