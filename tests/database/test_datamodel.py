"""XXX: depends on content from create_test_db.py"""


def test_proposition(proposition):
    assert len(proposition.supporters) == 1


def test_user_proposition(user):
    assert len(user.supports) == 2
    assert user in user.supports[0].supporters
