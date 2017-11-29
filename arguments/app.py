from datetime import datetime
import logging
import os
import jinja2
from more.transaction import TransactionApp
from morepath.reify import reify
from morepath.request import Request
from munch import Munch
from werkzeug.datastructures import ImmutableDict
from zope.sqlalchemy import register
import morepath
import yaml

from arguments.helper.templating import PyJadeExtension, select_jinja_autoescape
from arguments import database


logg = logging.getLogger(__name__)


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


class DBSessionRequest(Request):
    @reify
    def db_session(self):
        return database.Session()

    def q(self, *args, **kwargs):
        return self.db_session.query(*args, **kwargs)


def fake_translate(name, *a, **k):
    el = [str(e) for e in [name, a if a else None, list(k.values()) if k else None] if e]
    return ", ".join(el)


class App(TransactionApp):
    request_class = DBSessionRequest
    
    def __init__(self):
        super().__init__()
        jinja_globals = dict(url_for=lambda *a, **k: "#",
                             g=Munch(locale="de"),
                             current_user=Munch(is_authenticated=False),
                             _=fake_translate,
                             ngettext=fake_translate,
                             get_flashed_messages=lambda *a, **k: [],

                             )
        jinja_options = ImmutableDict(
            loader=jinja2.PackageLoader("arguments", "templates"),
            extensions=[PyJadeExtension, "jinja2.ext.autoescape"],
            autoescape=select_jinja_autoescape,
        )

        self.jinja_env = jinja2.Environment(**jinja_options)
        self.jinja_env.globals.update(jinja_globals)
        self.jinja_env.filters['datetimeformat'] = format_datetime
        self.jinja_env.filters['markdown'] = lambda t: t

    def render_template(self, template, **context):
        template = self.jinja_env.get_template(template)
        return template.render(**context)


def get_app_settings(settings_filepath):
    from arguments.default_settings import settings

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
        logg.warn("config file path %s doesn't exist!")

    return settings


def make_wsgi_app(args):
    morepath.autoscan()
    settings = get_app_settings(args.config_file)
    App.init_settings(settings)
    App.commit()

    app = App()
    database.configure_sqlalchemy(app.settings.database)
    return app
