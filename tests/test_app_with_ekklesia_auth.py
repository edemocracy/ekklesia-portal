import json
import time

import morepath
import responses
from ekklesia_common.ekklesia_auth import EkklesiaAuthData
from munch import Munch
from pytest import fixture
from webtest import TestApp as Client

from ekklesia_portal.app import create_or_update_user
from ekklesia_portal.datamodel import User
from tests.helpers.webtest_helpers import get_session


@fixture
def token():
    return {
        'token_type': 'bearer',
        'scope': 'test',
        'access_token': 'access',
        'refresh_token': 'refresh',
        'expires_at': time.time() + 100
    }


@fixture
def allow_insecure_transport(app, monkeypatch):
    monkeypatch.setenv('OAUTHLIB_INSECURE_TRANSPORT', "1")


@fixture
def client(app, allow_insecure_transport):
    return Client(app)


def test_create_or_update_user_should_create_new_user(db_session, req, ekklesia_auth_data: EkklesiaAuthData):
    create_or_update_user(req, Munch(dict(data=ekklesia_auth_data, token='token')))
    user = db_session.query(User).filter_by(name=ekklesia_auth_data.preferred_username).one()
    assert user.profile.sub == ekklesia_auth_data.sub
    assert user.profile.eligible == ekklesia_auth_data.eligible
    assert user.profile.verified == ekklesia_auth_data.verified


@responses.activate
def test_oauth_new_user(app, client, token):
    res = client.get('/ekklesia_auth/login')
    session = get_session(app, client)
    state = session['oauth_state']

    with responses.RequestsMock() as rsps:
        userinfo = {
            'sub': 'sub_new_user',
            'preferred_username': 'new_user',
            'roles': ['LV Bayern', 'BV'],
            'eligible': True,
            'verified': False
        }
        settings = app.settings.ekklesia_auth
        rsps.add(responses.GET, settings.userinfo_url, body=json.dumps(userinfo))  # @UndefinedVariable
        rsps.add(responses.POST, settings.token_url, body=json.dumps(token))  # @UndefinedVariable

        res = client.get(f'/ekklesia_auth/callback?code=deadbeef&state={state}', status=302)
        session = get_session(app, client)
        session_cookie = client.cookies['session']
        client.set_cookie('session', session_cookie)
        res = client.get('/ekklesia_auth/info')
        assert res.json == userinfo
