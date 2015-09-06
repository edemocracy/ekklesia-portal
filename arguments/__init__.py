import logging
from flask import Flask, g
from pprint import pformat
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin

logg = logging.getLogger(__name__)

app = None
db = None
admin = None


def make_app(**app_options):
    global db, app, admin

    app = Flask(__name__)
    app.jinja_env.add_extension('arguments.helper.templating.PyJadeExtension')
    logging.basicConfig(level=logging.INFO)
    logg.info("creating flask app %s", __name__)
    # app.config.from_object(arguments_config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://arguments:a@127.0.0.1/arguments"
    if app_options:
        app.config.update(app_options)
    logg.info("using database URI: '%s'", app.config["SQLALCHEMY_DATABASE_URI"])
    logg.debug("config is %s", pformat(dict(app.config)))

    app.config["RESTFUL_JSON"] = {'ensure_ascii': False}
    app.config["SECRET_KEY"] = "dev"
    db = SQLAlchemy(app)
    admin = Admin(app, name="Arguments", template_mode="bootstrap3")


    @app.before_request
    def load_user():
        """XXX: test user"""
        from arguments.database.datamodel import User    
        g.user = User.query.filter_by(login_name=u"testuser").one()

    import arguments.views
    import arguments.views.admin
    #import arguments_rest.api
    return app
