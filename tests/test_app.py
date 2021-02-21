import os
import morepath

from ekklesia_portal.app import get_app_settings

SETTING_SECTIONS = [
    "app", "babel_i18n", "browser_session", "common", "database", "ekklesia_auth", "importer", "share", "static_files"
]


def test_get_app_settings_none(monkeypatch):
    if "EKKLESIA_PORTAL_CONFIG" in os.environ:
        monkeypatch.delenv("EKKLESIA_PORTAL_CONFIG")
    settings = get_app_settings(None)
    assert settings == {}


def test_make_wsgi_app(app):
    assert isinstance(app, morepath.App)


def test_app_settings(app):
    for section in SETTING_SECTIONS:
        assert hasattr(app.settings, section)

    assert app.settings.common.instance_name == "test"


def test_app_babel_config(app):
    assert app.babel.domain.dirname.endswith("/ekklesia_portal/translations")
