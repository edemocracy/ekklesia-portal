import morepath
from munch import Munch
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


def test_identify(identity_policy, req, user_factory):
    user = user_factory()
    req.browser_session = {'user_id': user.id}
    identity = identity_policy.identify(req)
    assert identity.userid == user.id
    assert identity.has_global_admin_permissions is False


def test_identify_admin(identity_policy, req, user_factory, group_factory):
    group = group_factory(is_admin_group=True)
    user = user_factory()
    group.members.append(user)
    req.browser_session = {'user_id': user.id}
    identity = identity_policy.identify(req)
    assert identity.has_global_admin_permissions is True


def test_forget(identity_policy, req):
    req.browser_session = {'user_id': 1}
    identity_policy.forget(None, req)
    assert 'user_id' not in req.browser_session
