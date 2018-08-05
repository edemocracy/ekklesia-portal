import pytest
from ekklesia_portal.database.datamodel import Supporter

def test_proposition(db_session, user, user_two, proposition, proposition_two):
    supporters = [
        Supporter(proposition=proposition, member=user),
        Supporter(proposition=proposition, member=user_two),
        Supporter(proposition=proposition_two, member=user_two)
    ]
    db_session.add_all(supporters)

    assert len(proposition.supporters) == 2
    assert len(user.supports) == 1
    assert user_two in user.supports[0].supporters


@pytest.mark.parametrize('user__name', ['hans', 'wurst'])
def test_user(user, user__name):
    """This test isn't really useful but a good example for factory parametrization ;)"""
    assert user.name == user__name

