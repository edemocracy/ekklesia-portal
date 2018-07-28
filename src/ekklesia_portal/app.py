import logging
import os

import dectate
import jinja2
import morepath
from more.babel_i18n import BabelApp
from more.browser_session import BrowserSessionApp
from more.forwarded import ForwardedApp
from more.transaction import TransactionApp
import yaml

from ekklesia_portal import database
from ekklesia_portal.database.datamodel import User, UserProfile, OAuthToken
from ekklesia_portal.helper.cell import JinjaCellEnvironment
from ekklesia_portal.helper.templating import make_jinja_env
from ekklesia_portal.request import EkklesiaPortalRequest
from ekklesia_portal.ekklesia_auth import EkklesiaAuthApp, EkklesiaAuthPathApp
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy


logg = logging.getLogger(__name__)


class ConceptAction(dectate.Action):
    config = {
        'concepts': dict
    }

    def __init__(self, name):
        self.name = name

    def identifier(self, **_kw):
        return self.name

    def perform(self, obj, concepts):
        concepts[self.name] = obj


class App(ForwardedApp, TransactionApp, BabelApp, BrowserSessionApp, EkklesiaAuthApp):
    request_class = EkklesiaPortalRequest
    concept = dectate.directive(ConceptAction)

    def __init__(self):
        super().__init__()
        loader_mapping = {p: jinja2.PackageLoader(f"ekklesia_portal.concepts.{p}") for p in App.config.concepts}
        template_loader = jinja2.ChoiceLoader([jinja2.PrefixLoader(loader_mapping), jinja2.PackageLoader("ekklesia_portal")])
        self.jinja_env = make_jinja_env(jinja_environment_class=JinjaCellEnvironment, jinja_options=dict(loader=template_loader), app=self)


@App.identity_policy()
def get_identity_policy():
    return EkklesiaPortalIdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    return True


@App.after_oauth_callback()
def create_or_update_user(request, ekklesia_auth):
    auid = ekklesia_auth.auid['auid']
    profile = ekklesia_auth.profile
    membership = ekklesia_auth.membership
    token = ekklesia_auth.token
    name = profile['username']
    user_profile = request.q(UserProfile).filter_by(auid=auid).scalar()

    if user_profile is None:
        user_profile = UserProfile(auid=auid)
        oauth_token = OAuthToken(provider='ekklesia', token=token)
        user = User(name=name, auth_type='oauth', profile=user_profile, oauth_token=oauth_token)
        logg.debug("created new ekklesia user with auid %s, name %s", auid, name)
        request.db_session.add(user)
    else:
        user = user_profile.user
        user.name = profile['username']
        user.oauth_token.token = token
        logg.debug("updated ekklesia user with auid %s, name %s", auid, name)

    user_profile.user_type = membership.get('type')
    user_profile.verified = membership.get('verified')
    user_profile.profile = membership.get('profile')
    user_profile.avatar = membership.get('avatar')

    request.db_session.flush()

    @request.after
    def remember(response):
        identity = morepath.Identity(user.id, user=user)
        request.app.root.remember_identity(response, request, identity)


@App.get_oauth_token()
def get_oauth_token_from_user(app, request):
    logg.debug('get_oauth_token_from_user')
    user = request.current_user
    if user is None or user.auth_type != 'oauth':
        return None
    return user.oauth_token.token


@App.set_oauth_token()
def set_oauth_token_from_user(app, request, token):
    request.current_user.oauth_token = OAuthToken(provider='ekklesia', token=token)


@App.mount(path='ekklesia_auth', app=EkklesiaAuthPathApp)
def mount_ekklesia_auth_path():
    app = EkklesiaAuthPathApp()
    return app


def get_app_settings(settings_filepath):
    from ekklesia_portal.default_settings import settings

    if settings_filepath is None:
        logg.info("no config file given")
    elif os.path.isfile(settings_filepath):
        with open(settings_filepath) as config:
            settings_from_file = yaml.load(config)
        logg.info("loaded config from %s", settings_filepath)

        for section_name, section in settings_from_file.items():
            if section_name in settings:
                settings[section_name].update(section)
            else:
                settings[section_name] = section
    else:
        logg.warn("config file path %s doesn't exist!", settings_filepath)

    return settings


def get_locale(request):
    locale = request.browser_session.get('lang')
    if locale:
        logg.debug('locale from session: %s', locale)
    else:
        locale = request.accept_language.best_match(['de', 'en', 'fr'])
        logg.debug('locale from request: %s', locale)

    return locale


def make_wsgi_app(settings_filepath=None):
    morepath.autoscan()
    settings = get_app_settings(settings_filepath)
    App.init_settings(settings)
    EkklesiaAuthPathApp.init_settings(settings)
    App.commit()

    app = App()
    database.configure_sqlalchemy(app.settings.database)
    app.babel_init()
    app.babel.localeselector(get_locale)
    return app
