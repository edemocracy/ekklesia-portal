import time

from sqlalchemy import Column, ForeignKey, Table, event, Integer, DateTime, func as sqlfunc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship, backref, Query, Mapper
from sqlalchemy.ext.declarative import declared_attr

from arguments import db

rel = db.relationship
FK = db.ForeignKey
C = db.Column
Model = db.Model
Table = db.Table

SLOW_QUERY_SECONDS = 0.3

def dynamic_rel(*args, **kwargs):
    return rel(*args, lazy="dynamic", **kwargs)


class TimeStamp(object):

    """a simple timestamp mixin"""

    @declared_attr
    def created_at(cls):
        return C(DateTime, default=sqlfunc.now())


def integer_pk(**kwargs):
    return C(Integer, primary_key=True, **kwargs)


def integer_fk(*args, **kwargs):
    if len(args) == 2:
        return C(args[0], ForeignKey(args[1]), **kwargs)
    elif len(args) == 1:
        return C(ForeignKey(args[0]), **kwargs)
    else:
        raise ValueError("at least one argument must be specified (type)!")


# some pretty printing for SQLAlchemy objects ;)


def to_dict(self):
    return dict((str(col.name), getattr(self, col.name))
                for col in self.__table__.columns)


def to_yaml(self):
    return pyaml.dump(self.to_dict())


Model.to_dict = to_dict
Model.to_yaml = to_yaml


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    conn.info.setdefault('current_query', []).append(statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    # total in seconds
    if total > SLOW_QUERY_SECONDS:
        if hasattr(conn.connection.connection, "history"):
            statement = conn.connection.connection.history.last_statement
        else:
            statement = conn.info['current_query'].pop(-1)
        logg.warn("slow query %.1fms:\n%s", total * 1000, statement)

