from datetime import datetime
import logging
import os
import jinja2
import morepath
from munch import Munch
from werkzeug.datastructures import ImmutableDict
import yaml

from arguments.helper.templating import PyJadeExtension, select_jinja_autoescape


logg = logging.getLogger(__name__)


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


class App(morepath.App):
    def __init__(self):
        super().__init__()
        jinja_globals = dict(url_for=lambda *a, **k: "#",
                             g=Munch(locale="de"),
                             current_user=Munch(is_authenticated=False),
                             _=lambda name, *a, **k: name,
                             ngettext=lambda name, *a, **k: name,
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


def configure_app_settings(settings_filepath):
    if os.path.isfile(settings_filepath):

        with open(settings_filepath) as config:
            settings = yaml.load(config)

        App.init_settings(settings)
        logg.info("loaded config from %s", settings_filepath)
    else:
        logg.warn("config file path %s doesn't exist!")


def make_wsgi_app(args):
    morepath.autoscan()

    if args.config_file:
        configure_app_settings(args.config_file)
    else:
        logg.info("no config file given")

    App.commit()
    wsgi_app = App()
    return wsgi_app
