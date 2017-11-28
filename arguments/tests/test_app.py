import os
from os import path
import morepath
from munch import Munch
from arguments.app import make_wsgi_app

BASEDIR = os.path.dirname(__file__)


def test_make_wsgi_app():
    args = Munch(config_file=path.join(BASEDIR, "testconfig.yml"))
    app = make_wsgi_app(args)
    assert isinstance(app, morepath.App)
    assert app.settings.test_section.test_setting == "test"


def test_make_wsgi_app_config_not_present():
    args = Munch(config_file=None)
    app = make_wsgi_app(args)
    assert isinstance(app, morepath.App)
    assert app.settings