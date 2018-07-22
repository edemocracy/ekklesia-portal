from functools import partial
import logging
import dectate
from morepath import redirect, App, Request
from requests_oauthlib import OAuth2Session
from urllib.parse import urljoin
from ekklesia_portal.database.datamodel import UserProfile, User
from ekklesia_portal.helper.utils import cached_property


logg = logging.getLogger(__name__)


class EkklesiaNotAuthorized(Exception):
    pass


class EkklesiaAuth:
    """Wraps the OAuth2 session and provides helpers for Ekklesia ID server API access."""

    def __init__(self, settings, token=None, get_token=None, set_token=None):
        self.settings = settings
        if token is not None and get_token is not None:
            raise RuntimeError('token and get_token arguments cannot be used at the same time')
        if token is None and get_token is None:
            raise RuntimeError('one of the arguments token or get_token must be specified')
        self._get_token = get_token
        self._set_token = set_token
        self._token = token

    @cached_property
    def token(self):
        if self._token is not None:
            return self._token

        logg.debug('no token yet, using getter')
        return self._get_token()

    @cached_property
    def session(self):
        if not self.authorized:
            raise EkklesiaNotAuthorized()

        extra = {'client_secret': self.settings.client_secret}
        return OAuth2Session(token=self.token,
                             client_id=self.settings.client_id,
                             auto_refresh_url=self.settings.token_url,
                             auto_refresh_kwargs=extra,
                             token_updater=self._set_token)

    @property
    def authorized(self):
        return self.token is not None

    def api_request(self, method, path, **kwargs):
        url = urljoin(self.settings.api_base_url, path)
        res = self.session.request(method, url, **kwargs)
        return res.json()

    @cached_property
    def profile(self):
        return self.api_request('GET', 'user/profile')

    @cached_property
    def auid(self):
        return self.api_request('GET', 'user/auid')

    @cached_property
    def membership(self):
        return self.api_request('GET', 'user/membership')


class GetOAuthTokenAction(dectate.Action):
    config = {}
    app_class_arg = True

    def __init__(self):
        pass

    def identifier(self, **_kw):
        return ()

    def perform(self, obj, app_class):
        app_class._get_oauth_token = obj


class SetOAuthTokenAction(dectate.Action):
    config = {}
    app_class_arg = True

    def __init__(self):
        pass

    def identifier(self, **_kw):
        return ()

    def perform(self, obj, app_class):
        app_class._set_oauth_token = obj


class AfterAuthAction(dectate.Action):

    config = {
        'after_oauth_callbacks': dict
    }

    def __init__(self, name=None):
        self.name = name

    def identifier(self, **_kw):
        return self.name

    def perform(self, obj, after_oauth_callbacks):
        after_oauth_callbacks[obj.__name__] = obj


class EkklesiaAuthApp(App):
    """Provides Ekklesia authentication features to Morepath apps.
    Requests done via subclasses of this get an `ekklesia_auth` attribute which
    can be used for checking if authorization is granted and to retrieve data
    from the Ekklesia ID server API.
    """

    def _get_oauth_token(*_args, **_kw):
        raise Exception("not set")

    get_oauth_token = dectate.directive(GetOAuthTokenAction)

    def _set_oauth_token(*_args, **_kw):
        raise Exception("not set")

    set_oauth_token = dectate.directive(SetOAuthTokenAction)

    after_oauth_callback = dectate.directive(AfterAuthAction)


@EkklesiaAuthApp.setting_section(section='ekklesia_auth')
def ekklesia_auth_setting_section():
    return {
        'client_id': 'ekklesia_portal',
        'client_secret': "ekklesia_portal_secret",
        'api_base_url': "https://identity-server.invalid/api/v1/",
        'authorization_url': "https://identity-server.invalid/oauth2/authorize/",
        'token_url': "https://identity-server.invalid/oauth2/token/"
    }


@EkklesiaAuthApp.tween_factory()
def make_ekklesia_auth_tween(app, handler):
    def ekklesia_auth_tween(request):
        get_oauth_token = partial(app.root._get_oauth_token, request)
        set_oauth_token = partial(app.root._set_oauth_token, request)
        logg.debug('ekklesia_auth tween')
        request.ekklesia_auth = EkklesiaAuth(app.root.settings.ekklesia_auth, get_token=get_oauth_token, set_token=set_oauth_token)
        return handler(request)

    return ekklesia_auth_tween


class EkklesiaAuthPathApp(App):
    """Provides paths for getting OAuth2 authorization ("login") and info.
    Should be mounted under a App subclassing `EkklesiaApp`.
    """
    pass


class EkklesiaLogin:

    def __init__(self, settings=None, session=None):
        self.settings = settings
        self.session = session

    @cached_property
    def oauth(self):
        return OAuth2Session(client_id=self.settings.client_id)

    def get_authorization_url(self):
        authorization_url, state = self.oauth.authorization_url(self.settings.authorization_url)
        self.session["oauth_state"] = state
        return authorization_url


@EkklesiaAuthPathApp.path(model=EkklesiaLogin, path="/login")
def oauth_login(request):
    return EkklesiaLogin(request.app.root.settings.ekklesia_auth, request.browser_session)


@EkklesiaAuthPathApp.view(model=EkklesiaLogin)
def get_oauth_login(self, _):
    """redirect to login URL on ekklesia ID server"""
    return redirect(self.get_authorization_url())


class OAuthCallback:
    def __init__(self, request):
        self.request = request
        self.settings = request.app.root.settings.ekklesia_auth
        self.session = request.browser_session
        self.called_url = request.url
        self.oauth = OAuth2Session(client_id=self.settings.client_id, redirect_uri=request.link(self),
                                   state=self.session.get('oauth_state'))

    @property
    def redirect_after_success_url(self):
        return "/"

    def fetch_token(self):
        self.token = self.oauth.fetch_token(token_url=self.settings.token_url,
                                            authorization_response=self.called_url,
                                            client_secret=self.settings.client_secret)

    def after_auth(self):
        root_app = self.request.app.root
        if root_app.config.after_oauth_callbacks:
            ekklesia_auth = EkklesiaAuth(root_app.settings.ekklesia_auth, self.token)
            for callback in root_app.config.after_oauth_callbacks.values():
                callback(request=self.request, ekklesia_auth=ekklesia_auth)


@EkklesiaAuthPathApp.path(model=OAuthCallback, path="/callback")
def oauth_callback(request):
    return OAuthCallback(request)


@EkklesiaAuthPathApp.view(model=OAuthCallback)
def get_oauth_callback(self, _request):
    self.fetch_token()
    self.after_auth()
    return redirect(self.redirect_after_success_url)


class OAuthInfo:
    def __init__(self, ekklesia_auth):
        self.ekklesia_auth = ekklesia_auth

    @property
    def info(self):
        if not self.ekklesia_auth.authorized:
            logg.debug('oauth info: error not authorized')
            return {'error': 'not authorized'}

        return {
            'membership': self.ekklesia_auth.membership,
            'profile': self.ekklesia_auth.profile,
            'auid': self.ekklesia_auth.auid
        }


@EkklesiaAuthPathApp.path(model=OAuthInfo, path="/info")
def oauth_info(request):
    return OAuthInfo(request.ekklesia_auth)


@EkklesiaAuthPathApp.json(model=OAuthInfo)
def oauth_info_json(self, _):
    return self.info
