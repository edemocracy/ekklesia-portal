from munch import Munch
import morepath
from pytest import fixture
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy


@fixture
def identity_policy():
    return EkklesiaPortalIdentityPolicy()


@fixture
def identity():
    user = Munch(id=1)
    return morepath.Identity(userid=user.id, user=user)


def test_remember(identity_policy, identity, req):
    req.browser_session = {}
    identity_policy.remember(None, req, identity)
    assert req.browser_session['user_id'] == 1


def test_identify(identity_policy, req):
    req.browser_session = {'user_id': 1}
    identity_policy.identify(req)


def test_forget(identity_policy, req):
    req.browser_session = {'user_id': 1}
    identity_policy.forget(None, req)
    assert 'user_id' not in req.browser_session
