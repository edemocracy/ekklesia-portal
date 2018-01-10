import time
import json
from urllib.parse import urljoin
from pytest import fixture, raises

import morepath
import responses
from webtest import TestApp as Client

from ekklesia_portal.ekklesiaauth import EkklesiaAuthApp, EkklesiaAuthRequest, EkklesiaAuth, EkklesiaNotAuthorized


morepath.autoscan()

CLIENT_ID = 'client_id_test'
AUTHORIZATION_URL = 'http://id.invalid/oauth2/authorize/'
TOKEN_URL = 'http://id.invalid/oauth2/token/'
API_BASE_URL = "http://id.invalid/api/v1/"

EKKLESIAAUTH_SETTINGS = {
    'client_id': CLIENT_ID,
    'client_secret': "test_secret",
    'api_base_url': API_BASE_URL,
    'authorization_url': AUTHORIZATION_URL,
    'token_url': TOKEN_URL,
}


@fixture
def browser_session():
    return {}


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
def app(browser_session):
    class TestRequest(EkklesiaAuthRequest):
        @property
        def browser_session(self):
            return browser_session

    class TestApp(EkklesiaAuthApp):
        request_class = TestRequest
        pass

    @TestApp.setting_section(section='ekklesiaauth')
    def settings():
        return EKKLESIAAUTH_SETTINGS

    TestApp.commit()
    app = TestApp()
    return app


@fixture
def allow_insecure_transport(app, monkeypatch):
    monkeypatch.setenv('OAUTHLIB_INSECURE_TRANSPORT', "1")


@fixture
def client(app, allow_insecure_transport):
    return Client(app)


def test_make_app(app):
    settings = app.settings.ekklesiaauth
    assert settings.client_id == EKKLESIAAUTH_SETTINGS['client_id']


def test_oauth_login(client):
    res = client.get('/login', status=302)
    loc = res.headers['Location']
    assert loc.startswith(AUTHORIZATION_URL)
    assert CLIENT_ID in loc


@responses.activate
def test_oauth_callback(client, browser_session, token):
    responses.add(responses.POST, TOKEN_URL, body=json.dumps(token))  # @UndefinedVariable

    browser_session['oauth_state'] = 'eee'
    url = f'/callback?code=deadbeef&state=eee'
    res = client.get(url, status=302)
    loc = res.headers['Location']
    assert loc == 'http://localhost/'


def test_session_and_authorized(app, browser_session, token):
    browser_session['oauth_token'] = token
    ekklesiaauth = EkklesiaAuth(app.settings.ekklesiaauth, browser_session)
    assert ekklesiaauth.authorized
    assert ekklesiaauth.session


def test_not_authorized(app, browser_session):
    ekklesiaauth = EkklesiaAuth(app.settings.ekklesiaauth, browser_session)
    assert not ekklesiaauth.authorized
    with raises(EkklesiaNotAuthorized):
        ekklesiaauth.session


@responses.activate
def test_session(app, browser_session, allow_insecure_transport, token):
    browser_session['oauth_token'] = token
    req_url = urljoin(API_BASE_URL, 'fake')
    ekklesiaauth = EkklesiaAuth(app.settings.ekklesiaauth, browser_session)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, req_url, body="test")  # @UndefinedVariable
        res = ekklesiaauth.session.get(req_url)

    assert res.content == b'test'


@responses.activate
def test_session_token_refresh(app, browser_session, allow_insecure_transport, token):
    outdated_token = dict(token, expires_at=token['expires_at'] - 1000, access_token='outdated')
    browser_session['oauth_token'] = outdated_token
    refreshed_token = dict(token, access_token='refreshed')
    req_url = urljoin(API_BASE_URL, 'fake')
    ekklesiaauth = EkklesiaAuth(app.settings.ekklesiaauth, browser_session)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, TOKEN_URL, body=json.dumps(refreshed_token))  # @UndefinedVariable
        rsps.add(responses.GET, req_url, body="test")  # @UndefinedVariable
        ekklesiaauth.session.get(req_url)

    assert browser_session['oauth_token']['access_token'] == 'refreshed'


def test_oauth_dance(app, client, browser_session, token):
    client.get('/login')
    state = browser_session['oauth_state']
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, TOKEN_URL, body=json.dumps(token))  # @UndefinedVariable
        client.get(f'/callback?code=deadbeef&state={state}', status=302)

    with responses.RequestsMock() as rsps:
        auid = '39219407-03ae-49ee-b71c-3e837eecaf48'
        profile = {'avatar': False, 'username': 'test'}
        membership = {
            'all_nested_groups': [1, 2],
            'nested_groups': [1, 2],
            'type': 'system user',
            'verified': False
        }
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'profile'), body=json.dumps(profile))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'auid'), body=json.dumps(auid))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'membership'), body=json.dumps(membership))  # @UndefinedVariable

        res = client.get('/info')
        assert res.json['auid'] == auid
        assert res.json['profile'] == profile
        assert res.json['membership'] == membership
