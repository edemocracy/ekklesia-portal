import morepath
from pytest import fixture
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy
from ekklesia_portal.database.datamodel import User


@fixture
def identity_policy():
    return EkklesiaPortalIdentityPolicy()


@fixture
def user(request):
    return request.db_session.query(User).get(1)


@fixture
def identity(user):
    return morepath.Identity(userid=user.id, user=user)


def test_remember(identity_policy, identity, request):
    request.browser_session = {}
    identity_policy.remember(None, request, identity)
    assert request.browser_session['user_id'] == 1
    

def test_identify(identity_policy, request):
    request.browser_session = {'user_id': 1}
    res = identity_policy.identify(request)
    

def test_forget(identity_policy, request):
    request.browser_session = {'user_id': 1}
    identity_policy.forget(None, request)
    assert 'user_id' not in request.browser_session

    