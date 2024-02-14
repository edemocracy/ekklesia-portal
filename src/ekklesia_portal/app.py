import locale
import logging
import os
import random
import string

import morepath
import reg
import yaml
import ekklesia_common
from ekklesia_common import database
from ekklesia_common.app import EkklesiaBrowserApp
from ekklesia_common.ekklesia_auth import EkklesiaAuth, EkklesiaAuthPathApp
from ekklesia_common.lid import LID
from eliot import log_call, start_action, log_message

import ekklesia_portal
from ekklesia_portal.datamodel import Department, Group, OAuthToken, User, UserProfile
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy

logg = logging.getLogger(__name__)


class BaseApp(EkklesiaBrowserApp):
    package_name = 'ekklesia_portal'


class App(BaseApp):
    pass


@BaseApp.setting_section(section="app")
def app_setting_section():
    return {
        "custom_footer_url": None,
        "data_protection_url": None,
        "default_proposition_query": {
            "status": "draft,submitted,qualified,scheduled,voting"
        },
        "enable_amendments": True,
        "enable_counter_propositions": True,
        "enable_drafts": True,
        "submit_proposition_as_hidden": True,
        "fallback_language": "de",
        "faq_url": None,
        "imprint_url": None,
        "insecure_development_mode": False,
        "log_environment_on_startup": False,
        "internal_login_enabled": True,
        "languages": ["de", "en"],
        "timezone": "UTC",
        "login_visible": False,
        "report_url": None,
        "source_code_url": "https://github.com/edemocracy/ekklesia-portal",
        "title": "Ekklesia Portal Dev",
        "tos_url": None,
    }


@BaseApp.setting_section(section="database")
def database_setting_section():
    return {"uri": "postgresql+psycopg2://ekklesia_portal:ekklesia_portal@127.0.0.1/ekklesia_portal"}


@BaseApp.setting_section(section="share")
def share_setting_section():
    return {
        "use_url_shortener": False,
        "hashtag": '',
        "promote_account": '',
        "email_topic": {
            "en": "Ekklesia Portal - Share Proposition",
            "de": "Ekklesia Portal - Teile Antrag"
        },
        "email_body": {
            "en": "I just wanted to share a proposition from the Ekklesia Portal!\n",
            "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!\n"
        },
        "tweet_msg": {
            "en": "I just wanted to share a proposition from the Ekklesia Portal!",
            "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!"
        },
    }


def _convert_lid_or_legacy_id(value):
    if "-" not in value:
        return LID(int(value))
    else:
        return LID.from_str(value)


@App.converter(type=LID)
def convert_lid():
    return morepath.Converter(lambda s: _convert_lid_or_legacy_id(s), lambda l: str(l))


@App.identity_policy()
def get_identity_policy():
    return EkklesiaPortalIdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    return True


@App.after_oauth_callback()
def create_or_update_user(request, ekklesia_auth: EkklesiaAuth) -> None:
    _ = request.i18n.gettext

    try:
        userinfo = ekklesia_auth.data
    except TypeError:
        request.flash(
            _(
                "alert_ekklesia_auth_failed_parsing"
            ), "danger"
        )
        return

    sub = userinfo.sub
    token = ekklesia_auth.token

    if userinfo.preferred_username:
        name = userinfo.preferred_username
    else:
        name = "user_" + "".join(random.choice(string.ascii_lowercase) for x in range(10))

    auth_settings = request.app.root.settings.ekklesia_auth

    required_role_for_login = auth_settings.required_role_for_login

    if required_role_for_login is not None and required_role_for_login not in userinfo.roles:
        request.flash(
            _(
                "alert_ekklesia_login_not_allowed",
                name=auth_settings.display_name,
                role=auth_settings.required_role_for_login
            ), "danger"
        )
        return
    else:
        request.flash(_("alert_logged_in_to", name=auth_settings.display_name), "success")

    user_profile: UserProfile = request.q(UserProfile).filter_by(sub=sub).scalar()

    if user_profile is None:
        user_profile = UserProfile(sub=sub)
        oauth_token = OAuthToken(provider='ekklesia', token=token)
        user = User(name=name, auth_type='oauth', profile=user_profile, oauth_token=oauth_token)
        logg.debug("created new ekklesia user with sub %s, name %s", sub, name)
        request.db_session.add(user)
    else:
        user = user_profile.user
        user.name = name
        user.oauth_token.token = token
        logg.debug("updated ekklesia user with sub %s, name %s", sub, name)

    user_profile.eligible = userinfo.eligible
    user_profile.verified = userinfo.verified

    departments = request.q(Department).filter(Department.name.in_(userinfo.roles)).all()
    user.departments = departments

    groups = request.q(Group).filter(Group.name.in_(userinfo.roles)).all()
    user.groups = groups

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


@App.predicate(App.get_view, name='media_type', default=None,
               index=reg.KeyIndex)
def media_type_predicate(self, request, obj):
    return request.params.get("media_type")


@log_call(include_result=False)
def get_app_settings(settings_filepath=None):
    settings = {}

    if settings_filepath is None:
        settings_filepath = os.environ.get('EKKLESIA_PORTAL_CONFIG')

    if settings_filepath is None:
        logg.info("no config file given, using defaults")
    elif os.path.isfile(settings_filepath):
        with open(settings_filepath) as config:
            settings = yaml.safe_load(config)
        logg.info("loaded config from %s", settings_filepath)
    else:
        logg.warn("config file path %s doesn't exist!", settings_filepath)

    return settings


@log_call
def get_database_uri_for_alembic():
    # Get the URL from the config file, if there is one
    settings = get_app_settings()
    db_uri = settings.get("database", {}).get("uri")

    # No URL from the config file (or no config file), we have to fire up the
    # App to get the default database URI
    if db_uri is None:
        App.commit()
        app = App()
        db_uri = app.settings.database.uri

    return db_uri


@log_call
def get_locale(request):
    locale = request.browser_session.get('lang')
    if locale:
        logg.debug('locale from session: %s', locale)
    else:
        locale = request.accept_language.best_match(request.app.root.settings.app.languages)
        logg.debug('locale from request: %s', locale)

    return locale


@log_call
def make_wsgi_app(settings_filepath=None, testing=False):
    with start_action(action_type='morepath_scan'):
        morepath.scan(ekklesia_common)
        morepath.scan(ekklesia_portal)

    if testing:
        log_message(message_type="testing", msg="running in testing mode, not loading any config from file")
    else:
        with start_action(action_type='settings'):
            settings = get_app_settings(settings_filepath)
            App._loaded_settings = settings
            App.init_settings(settings)

    with start_action(action_type='make_app'):
        App.commit()
        app = App()

    if app.settings.app.log_environment_on_startup:
        log_message(
            message_type="environment",
            env=dict(os.environ),
            encoding=locale.getpreferredencoding(),
            default_locale=locale.getdefaultlocale(),
            settings=settings,
        )

    database.configure_sqlalchemy(app.settings.database, testing)
    app.babel_init()
    app.babel.localeselector(get_locale)
    app.babel.timezoneselector(lambda: app.settings.app.timezone)

    return app
