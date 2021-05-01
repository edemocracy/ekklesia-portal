import pytest

from ekklesia_portal.datamodel import Supporter


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


def test_managed_departments(department_admin):
    managed = department_admin.managed_departments
    assert len(managed) == 1
    assert managed[0].description == 'admin'


def test_user_add_group(db_session, user, group):
    user.groups.append(group)


@pytest.mark.parametrize('user__name', ['hans', 'wurst'])
def test_user(user, user__name):
    """This test isn't really useful but a good example for factory parametrization ;)"""
    assert user.name == user__name
