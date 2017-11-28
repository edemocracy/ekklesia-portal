import os
from os import path
import morepath
from munch import Munch
from arguments.app import make_wsgi_app, get_app_settings

BASEDIR = os.path.dirname(__file__)


def test_get_app_settings_default():
    settings = get_app_settings(None)
    assert "app" in settings
    assert settings["app"]["instance_name"] == "arguments"
    

def test_get_app_settings():
    settings = get_app_settings(path.join(BASEDIR, "testconfig.yml"))
    assert "app" in settings
    assert "test_section" in settings
    assert settings["app"]["instance_name"] == "test"
    assert settings["test_section"]["test_setting"] == "test"
    

def test_make_wsgi_app():
    args = Munch(config_file=path.join(BASEDIR, "testconfig.yml"))
    app = make_wsgi_app(args)
    assert isinstance(app, morepath.App)
    assert app.settings.test_section.test_setting == "test"
    assert app.settings.app.instance_name == "test"
