"""XXX: depends on content from create_test_db.py"""
from pytest import fixture
from ekklesia_portal.database import Session
from ekklesia_portal.database.datamodel import Proposition


def test_proposition(proposition):
    assert len(proposition.supporters) == 1


def test_user_proposition(user):
    assert len(user.supports) == 2
    assert user in user.supports[0].supporters
