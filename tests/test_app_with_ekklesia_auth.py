import time
import json
from urllib.parse import urljoin
from pytest import fixture, raises

import morepath
from munch import Munch
import responses
from webtest import TestApp as Client


morepath.autoscan()

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


def decode_session(app, client):
    serializer = app.browser_session_interface.get_signing_serializer(app)
    return serializer.loads(client.cookies['session'])

@responses.activate
def test_oauth_new_user(app, client, token):
    res = client.get('/ekklesia_auth/login')
    session = decode_session(app, client)
    state = session['oauth_state']

    with responses.RequestsMock() as rsps:
        auid = {'auid': 'auid_new_user'}
        profile = {'avatar': 'ava', 'username': 'new_user'}
        membership = {
            'all_nested_groups': [1, 2],
            'nested_groups': [1, 2],
            'type': 'eligible member',
            'verified': False
        }
        settings = app.settings.ekklesia_auth
        rsps.add(responses.GET, urljoin(settings.api_base_url, 'user/profile'), body=json.dumps(profile))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(settings.api_base_url, 'user/auid'), body=json.dumps(auid))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(settings.api_base_url, 'user/membership'), body=json.dumps(membership))  # @UndefinedVariable
        rsps.add(responses.POST, settings.token_url, body=json.dumps(token))  # @UndefinedVariable

        res = client.get(f'/ekklesia_auth/callback?code=deadbeef&state={state}', status=302)
        session = decode_session(app, client)
        session_cookie = client.cookies['session']
        client.set_cookie('session', session_cookie)
        res = client.get('/ekklesia_auth/info')
        assert 'error' not in res.json
        assert res.json['auid'] == auid
        assert res.json['profile'] == profile
        assert res.json['membership'] == membership
