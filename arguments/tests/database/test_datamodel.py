"""XXX: depends on content from create_test_db.py"""
from pytest import fixture
from arguments.database import Session
from arguments.database.datamodel import Proposition


@fixture
def session(app):
    return Session()


@fixture
def proposition(session):
    return session.query(Proposition).get(1)


def test_proposition(proposition):
    assert len(proposition.supporters) == 1
