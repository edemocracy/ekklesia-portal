import time
import json
from urllib.parse import urljoin
from pytest import fixture, raises

import morepath
from munch import Munch
import responses
from webtest import TestApp as Client

from ekklesia_portal.ekklesia_auth import EkklesiaAuthApp, EkklesiaAuthPathApp, EkklesiaAuth, EkklesiaNotAuthorized


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
    return Munch()


@fixture
def fake_request_with_session(browser_session):
    return Munch(browser_session=browser_session)


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
def test_request_class(browser_session):
    class TestRequest(morepath.Request):

        @property
        def browser_session(self):
            return browser_session

    return TestRequest


@fixture
def req(test_request_class):
    return test_request_class()


@fixture
def app(test_request_class, browser_session):

    class TestApp(EkklesiaAuthApp):
        request_class = test_request_class

    @TestApp.mount(path='ekklesia_auth', app=EkklesiaAuthPathApp)
    def mount_ekklesia_auth_path():
        app = EkklesiaAuthPathApp()
        return app

    @TestApp.setting_section(section='ekklesia_auth')
    def settings():
        return EKKLESIAAUTH_SETTINGS

    @TestApp.get_oauth_token()
    def get_oauth_token(app, req):
        return browser_session.get('oauth_token')

    @TestApp.set_oauth_token()
    def set_oauth_token(app, req, token):
        browser_session['oauth_token'] = token

    @TestApp.after_oauth_callback()
    def after_oauth_callback(req, ekklesia_auth):
        browser_session['oauth_token'] = ekklesia_auth.token

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
    settings = app.settings.ekklesia_auth
    assert settings.client_id == EKKLESIAAUTH_SETTINGS['client_id']


def test_ekklesia_auth_app_config():

    class TestApp(EkklesiaAuthApp):
        pass

    @TestApp.after_oauth_callback()
    def after_auth_first(_req, _ekklesia_auth):
        pass

    @TestApp.after_oauth_callback('second')
    def after_auth_second(_req, _ekklesia_auth):
        pass

    @TestApp.set_oauth_token()
    def set_oauth_token():
        pass

    @TestApp.get_oauth_token()
    def get_oauth_token():
        pass

    TestApp.commit()
    app = TestApp()

    assert 'after_auth_first' in app.config.after_oauth_callbacks
    assert 'after_auth_second' in app.config.after_oauth_callbacks
    # config should overwrite default noop methods
    assert TestApp._get_oauth_token != EkklesiaAuthApp._get_oauth_token
    assert TestApp._set_oauth_token != EkklesiaAuthApp._set_oauth_token


def test_login_should_redirect_to_auth_url(client):
    res = client.get('/ekklesia_auth/login', status=302)
    loc = res.headers['Location']
    assert loc.startswith(AUTHORIZATION_URL)
    assert CLIENT_ID in loc


@responses.activate
def test_oauth_callback(client, browser_session, token):
    responses.add(responses.POST, TOKEN_URL, body=json.dumps(token))  # @UndefinedVariable

    browser_session['oauth_state'] = 'eee'
    url = f'/ekklesia_auth/callback?code=deadbeef&state=eee'
    res = client.get(url, status=302)
    loc = res.headers['Location']
    assert loc == 'http://localhost/'


def test_session_and_authorized(app, token):
    ekklesia_auth = EkklesiaAuth(app.settings.ekklesia_auth, token)
    assert ekklesia_auth.authorized
    assert ekklesia_auth.session


def test_no_token(app):
    with raises(RuntimeError):
        EkklesiaAuth(app.settings.ekklesia_auth, token=None)


def test_not_authorized(app):
    ekklesia_auth = EkklesiaAuth(app.settings.ekklesia_auth, get_token=lambda *a, **k: None)
    assert not ekklesia_auth.authorized
    with raises(EkklesiaNotAuthorized):
        ekklesia_auth.session


@responses.activate
def test_session(app, allow_insecure_transport, fake_request_with_session, token):
    request = fake_request_with_session
    request.browser_session.oauth_token = token
    req_url = urljoin(API_BASE_URL, 'fake')
    ekklesia_auth = EkklesiaAuth(app.settings.ekklesia_auth, token)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, req_url, body="test")  # @UndefinedVariable
        res = ekklesia_auth.session.get(req_url)

    assert res.content == b'test'


@responses.activate
def test_session_token_refresh(app, browser_session, allow_insecure_transport, token, fake_request_with_session):
    outdated_token = dict(token, expires_at=token['expires_at'] - 1000, access_token='outdated')
    browser_session.oauth_token = outdated_token
    refreshed_token = dict(token, access_token='refreshed')
    req_url = urljoin(API_BASE_URL, 'fake')

    def set_token(token):
        browser_session['oauth_token'] = token

    ekklesia_auth = EkklesiaAuth(app.settings.ekklesia_auth, outdated_token, set_token=set_token)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, TOKEN_URL, body=json.dumps(refreshed_token))  # @UndefinedVariable
        rsps.add(responses.GET, req_url, body="test")  # @UndefinedVariable
        ekklesia_auth.session.get(req_url)

    assert browser_session['oauth_token']['access_token'] == 'refreshed'


@responses.activate
def test_oauth_dance(app, client, browser_session, token):

    client.get('/ekklesia_auth/login')
    state = browser_session['oauth_state']

    with responses.RequestsMock() as rsps:
        auid = {'auid': 'auid_egon'}
        profile = {'avatar': False, 'username': 'test', 'profile': 'profile'}
        membership = {
            'all_nested_groups': [1, 2],
            'nested_groups': [1, 2],
            'type': 'system user',
            'verified': False
        }
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'user/profile'), body=json.dumps(profile))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'user/auid'), body=json.dumps(auid))  # @UndefinedVariable
        rsps.add(responses.GET, urljoin(API_BASE_URL, 'user/membership'), body=json.dumps(membership))  # @UndefinedVariable
        rsps.add(responses.POST, TOKEN_URL, body=json.dumps(token))  # @UndefinedVariable

        client.get(f'/ekklesia_auth/callback?code=deadbeef&state={state}', status=302)
        res = client.get('/ekklesia_auth/info')
        assert res.json['auid'] == auid
        assert res.json['profile'] == profile
        assert res.json['membership'] == membership
