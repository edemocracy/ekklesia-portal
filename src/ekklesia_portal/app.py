import logging
import os

from ekklesia_common import database
from ekklesia_common.app import EkklesiaBrowserApp
from ekklesia_common.ekklesia_auth import EkklesiaAuth, EkklesiaAuthPathApp, OAuthToken
from eliot import start_task, start_action, log_call
import morepath
import yaml

import ekklesia_portal
from ekklesia_portal.datamodel import User, UserProfile, Department
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy


logg = logging.getLogger(__name__)


class App(EkklesiaBrowserApp):
    package_name = 'ekklesia_portal'


@App.tween_factory()
def make_ekklesia_log_tween(app, handler):
    def ekklesia_log_tween(request):
        request_data = {
            'url': request.url,
            'headers': dict(request.headers)
        }

        user = request.current_user

        if user is not None:
            request_data['user'] = user.id

        with start_task(action_type='request', request=request_data):
            return handler(request)

    return ekklesia_log_tween


@App.tween_factory()
def make_ekklesia_customizations_tween(app, handler):
    def ekklesia_customizations_tween(request):
        if app.settings.app.force_ssl:
            request.scheme = 'https'

        return handler(request)

    return ekklesia_customizations_tween


@App.identity_policy()
def get_identity_policy():
    return EkklesiaPortalIdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    return True


@App.after_oauth_callback()
def create_or_update_user(request, ekklesia_auth: EkklesiaAuth) -> None:
    userinfo = ekklesia_auth.data
    auid = userinfo.auid
    token = ekklesia_auth.token
    name = userinfo.preferred_username
    user_profile: UserProfile = request.q(UserProfile).filter_by(auid=auid).scalar()

    if user_profile is None:
        user_profile = UserProfile(auid=auid)
        oauth_token = OAuthToken(provider='ekklesia', token=token)
        user = User(name=name, auth_type='oauth', profile=user_profile, oauth_token=oauth_token)
        logg.debug("created new ekklesia user with auid %s, name %s", auid, name)
        request.db_session.add(user)
    else:
        user = user_profile.user
        user.name = name
        user.oauth_token.token = token
        logg.debug("updated ekklesia user with auid %s, name %s", auid, name)

    user_profile.eligible = userinfo.eligible
    user_profile.verified = userinfo.verified

    departments = request.q(Department).filter(Department.name.in_(userinfo.roles)).all()
    user.departments = departments

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


@log_call
def get_app_settings(settings_filepath=None):
    from ekklesia_portal.default_settings import settings

    if settings_filepath is None:
        settings_filepath = os.environ.get('EKKLESIA_PORTAL_CONFIG')

    if settings_filepath is None:
        logg.info("no config file given, using defaults")
    elif os.path.isfile(settings_filepath):
        with open(settings_filepath) as config:
            settings_from_file = yaml.safe_load(config)
        logg.info("loaded config from %s", settings_filepath)

        for section_name, section in settings_from_file.items():
            if section_name in settings:
                settings[section_name].update(section)
            else:
                settings[section_name] = section
    else:
        logg.warn("config file path %s doesn't exist!", settings_filepath)

    return settings


@log_call
def get_locale(request):
    locale = request.browser_session.get('lang')
    if locale:
        logg.debug('locale from session: %s', locale)
    else:
        locale = request.accept_language.best_match(['de', 'en', 'fr'])
        logg.debug('locale from request: %s', locale)

    return locale


@log_call
def make_wsgi_app(settings_filepath=None, testing=False):
    with start_action(action_type='morepath_scan'):
        morepath.autoscan()
        morepath.scan(ekklesia_portal)

    with start_action(action_type='settings'):
        settings = get_app_settings(settings_filepath)
        App.init_settings(settings)
        EkklesiaAuthPathApp.init_settings(settings)

    with start_action(action_type='make_app'):
        App.commit()
        app = App()

    database.configure_sqlalchemy(app.settings.database, testing)
    app.babel_init()
    app.babel.localeselector(get_locale)
    return app
