import logging
from flask import Flask, g, request, session
from pprint import pformat
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel
from flask_admin import Admin
from flask_oauthlib.client import OAuth

logg = logging.getLogger(__name__)

app = None
db = None
admin = None
idserver = None

def init_oauth(app):
    global idserver
    oauth = OAuth(app)
    idserver = oauth.remote_app(
            'ekklesia',
            base_url='https://beoauth.piratenpartei-bayern.de/',
            access_token_url="oauth2/token/",
            authorize_url="oauth2/authorize/",
            app_key="EKKLESIA") 

    @idserver.tokengetter
    def get_idserver_token():
        resp = session['idserver']
        token = resp['access_token']
        print(token)
        return (token, '')

    return oauth


def make_app(**app_options):
    global db, app, admin

    app = Flask(__name__)
    app.jinja_env.add_extension('arguments.helper.templating.PyJadeExtension')
    logging.basicConfig(level=logging.DEBUG)
    logg.debug("creating flask app %s", __name__)
    try:
        import arguments.config
        app.config.from_object(arguments.config)
    except ImportError:
        pass

    if app_options:
        app.config.update(app_options)

    app.config["RESTFUL_JSON"] = {'ensure_ascii': False}
    app.config["SECRET_KEY"] = "dev"

    logg.debug("app config is:\n%s", pformat(dict(app.config)))

    @app.before_request
    def load_user():
        """XXX: test user"""
        from arguments.database.datamodel import User    
        g.user = User.query.filter_by(login_name=u"testuser").one()

    # initialize extension
    # flask-sqlalchemy
    db = SQLAlchemy(app)
    # flask-admin
    admin = Admin(app, name="Arguments", template_mode="bootstrap3")
    # i18n via flask-babelex
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        locale = request.accept_languages.best_match(['de', 'en', 'fr'])
        logg.debug("locale from request: %s", locale)
        return locale

    init_oauth(app)

    import arguments.views
    import arguments.views.admin
    #import arguments_rest.api
    return app
