from datetime import datetime
import os.path
import jinja2.runtime
from more.babel_i18n.request_utils import BabelRequestUtils
from pytest import fixture
from ekklesia_portal.helper.templating import make_jinja_env

TEST_DATETIME = datetime(2017, 1, 1, 11, 23, 42)
TEST_DATETIME_FORMATTED = "Jan 1, 2017, 11:23:42 AM"


class JinjaTestContext(jinja2.runtime.Context):
    pass


class JinjaTestEnvironment(jinja2.Environment):
    context_class = JinjaTestContext


@fixture
def jinja_env(app):
    template_loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
    jinja_env = make_jinja_env(jinja_environment_class=JinjaTestEnvironment, jinja_options=dict(loader=template_loader), app=app)
    return jinja_env


@fixture
def render_string(jinja_env, req):
    req.i18n = BabelRequestUtils(req)
    req.i18n.babel.locale_selector_func = None
    req.browser_session = {}

    def render_string(template_string, **ctx):
        template = jinja_env.from_string(template_string)
        res = template.render(_request=req, **ctx)
        return res

    return render_string


def test_render_string(render_string):
    res = render_string("{{ x }}", x=5)
    assert res == "5"


def test_filter_datetimeformat(render_string):
    dt = TEST_DATETIME
    res = render_string("{{ dt|datetimeformat }}", dt=dt)
    assert res == TEST_DATETIME_FORMATTED


def test_filter_scientificformat(render_string):
    x = 1_000_000
    res = render_string("{{ x|scientificformat }}", x=x)
    assert res == "1E6"


def test_filter_datetimeformat_in_germany(app, render_string):
    app.settings.babel_i18n.default_locale = "de_DE"
    app.settings.babel_i18n.default_timezone = "Europe/Berlin"
    dt = datetime(2017, 1, 1, 11, 23, 42)
    res = render_string("{{ dt|datetimeformat }}", dt=dt)
    assert res == "01.01.2017, 12:23:42"


def test_translation(app, render_string):
    app.settings.babel_i18n.default_locale = "en_US"
    res = render_string("{{ _('terms_of_use') }}")
    assert res == "Terms of Use"


def test_translation_with_args(app, render_string):
    app.settings.babel_i18n.default_locale = "en_US"
    res = render_string("{{ _('authored_at', dt=datestring) }}", datestring=TEST_DATETIME_FORMATTED)
    assert res == f"Added at {TEST_DATETIME_FORMATTED}"
