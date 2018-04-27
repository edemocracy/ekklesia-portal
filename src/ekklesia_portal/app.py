import logging
import os

import jinja2
import morepath
from more.babel_i18n import BabelApp
from more.browser_session import BrowserSessionApp
from more.transaction import TransactionApp
import yaml

from ekklesia_portal import database
from ekklesia_portal.helper.cell import JinjaCellEnvironment
from ekklesia_portal.helper.templating import make_jinja_env
from ekklesia_portal.request import EkklesiaPortalRequest
from ekklesia_portal.ekklesia_auth import EkklesiaAuthApp, EkklesiaAuthPathApp
from ekklesia_portal.identity_policy import EkklesiaPortalIdentityPolicy


logg = logging.getLogger(__name__)


class App(TransactionApp, BabelApp, BrowserSessionApp, EkklesiaAuthApp):
    request_class = EkklesiaPortalRequest

    def __init__(self):
        super().__init__()
        template_loader = jinja2.PackageLoader("ekklesia_portal")
        self.jinja_env = make_jinja_env(jinja_environment_class=JinjaCellEnvironment, jinja_options=dict(loader=template_loader), app=self)


@App.identity_policy()
def get_identity_policy():
    return EkklesiaPortalIdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    return True


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


def make_wsgi_app(settings_filepath=None):
    morepath.autoscan()
    settings = get_app_settings(settings_filepath)
    App.init_settings(settings)
    EkklesiaAuthPathApp.init_settings(settings)
    App.commit()

    app = App()
    database.configure_sqlalchemy(app.settings.database)
    app.babel_init()
    return app
