import logging
import os
import jinja2
from more.transaction import TransactionApp
import more.itsdangerous
from more.babel_i18n import BabelApp, BabelRequest
from morepath.reify import reify
from morepath.request import Request
import morepath
import yaml

from ekklesia_portal.helper.templating import make_jinja_env
from ekklesia_portal import database
from ekklesia_portal.helper.cell import JinjaCellEnvironment


logg = logging.getLogger(__name__)


class CustomRequest(BabelRequest):

    @reify
    def db_session(self):
        return database.Session()

    def q(self, *args, **kwargs):
        return self.db_session.query(*args, **kwargs)

    def render_template(self, template, **context):
        template = self.app.jinja_env.get_template(template)
        return template.render(**context)


class App(TransactionApp, BabelApp):
    request_class = CustomRequest

    def __init__(self):
        super().__init__()
        template_loader = jinja2.PackageLoader("ekklesia_portal")
        self.jinja_env = make_jinja_env(jinja_environment_class=JinjaCellEnvironment, jinja_options=dict(loader=template_loader), app=self)


@App.identity_policy()
def get_identity_policy():
    # XXX: secure=False only for testing
    return more.itsdangerous.IdentityPolicy(secure=False)


@App.verify_identity()
def verify_identity(identity):
    return True


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
    App.commit()

    app = App()
    database.configure_sqlalchemy(app.settings.database)
    app.babel_init()
    return app
