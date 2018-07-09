import logging
import os
import sys
#from flask import Flask, g, request, session, flash, redirect, url_for
from pprint import pformat
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.babelex import Babel, _
#from flask_admin import Admin
#from flask_dance.consumer import OAuth2ConsumerBlueprint, oauth_authorized, oauth_error
#from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
#from flask.ext.misaka import Misaka
#from flask_login import current_user, LoginManager, login_user
from werkzeug.contrib.fixers import ProxyFix


logg = logging.getLogger(__name__)

app = None
db = None
admin = None
ekklesia = None


def init_oauth_ext(app):
    """Configures the OAuth extension 'flask-dance' for use with the ekklesia ID server"""
    from ekklesia_portal.database.datamodel import EkklesiaUserInfo, User, OAuthToken
    global ekklesia

    ekklesia = OAuth2ConsumerBlueprint(
            'ekklesia', __name__,
            client_id=app.config["EKKLESIA_CLIENT_ID"],
            client_secret=app.config["EKKLESIA_CLIENT_SECRET"],
            base_url=app.config["EKKLESIA_API_BASE_URL"],
            token_url=app.config["EKKLESIA_TOKEN_URL"],
            authorization_url=app.config["EKKLESIA_AUTHORIZATION_URL"])

    app.register_blueprint(ekklesia, url_prefix="/login")

    ekklesia.backend = SQLAlchemyBackend(OAuthToken, db.session, user=current_user)

    # create/login local user on successful Ekklesia login
    @oauth_authorized.connect_via(ekklesia)
    def ekklesia_logged_in(blueprint, token):

        auth_title = app.config["EKKLESIA_TITLE"]
        if not token:
            flash(_("login_fail_with", auth_title=auth_title))
            return

        # ekklesia users have an unique auid, try to find an existing user in our database by auid
        res_auid = ekklesia.session.get("user/auid/")
        if res_auid.ok:
            auid = res_auid.json()["auid"]
            user = User.query.join(EkklesiaUserInfo).filter_by(auid=auid).scalar()
            # get user profile for more info
            res_profile = ekklesia.session.get("user/profile/")
            res_membership = ekklesia.session.get("user/membership/")

            if res_profile.ok and res_membership.ok:
                profile = res_profile.json()
                membership = res_membership.json()

                display_name = profile["username"]

                if user is None:
                    user = User(login_name=auid, display_name=display_name)
                    user.ekklesia_info = EkklesiaUserInfo(auid=auid, user=user)
                    db.session.add(user)
                    logg.info("creating user with auid %s", auid)
                else:
                    # just update user data
                    logg.info("updating user with auid %s", auid)

                user.ekklesia_info.update(
                    user_type=membership["type"],
                    verified=membership["verified"],
                    all_nested_group_ids=membership["all_nested_groups"],
                    nested_group_ids=membership["nested_groups"]
                )

                db.session.commit()
                login_user(user)
                flash(_("login_success_with", auth_title=auth_title))

                next_url = request.args.get('next')
                redirect(next_url or url_for('propositions'))

            else:
                flash("Failed to fetch user profile from Ekklesia ID Server", category="error")
        else:
            flash("Failed to fetch user id from Ekklesia ID Server", category="error")

    @oauth_error.connect_via(ekklesia)
    def ekklesia_error(blueprint, error, error_description=None, error_uri=None):
        msg = "OAuth error from Ekklesia! error={error} description={description} uri={uri}".format(
            error=error, description=error_description, uri=error_uri)

        flash(msg, category="error")

    return ekklesia


def make_app(debug=False, **app_options):
    global db, app, admin

    app = Flask(__name__)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logg.debug("creating flask app %s", __name__)
    try:
        import ekklesia_portal.config
        app.config.from_object(ekklesia_portal.config)
    except ImportError:
        pass

    if app_options:
        app.config.update(app_options)

    app.config["RESTFUL_JSON"] = {'ensure_ascii': False}
    app.config["SECRET_KEY"] = "dev"
    app.config["DEBUG"] = debug
    logg.debug("app config is:\n%s", pformat(dict(app.config)))

    if debug:
        app.debug = True
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    app.jinja_env.add_extension('ekklesia_portal.helper.templating.PyJadeExtension')

    # initialize extensions
    # flask-sqlalchemy
    db = SQLAlchemy(app)
    import ekklesia_portal.database.datamodel

    # flask-admin
    admin = Admin(app, name="ekklesia_portal", template_mode="bootstrap3")

    # markdown via flask-misaka
    # TODO: markdown options should be configurable
    markdown_opts = dict(
        autolink=True,
        fenced_code=True,
        no_intra_emphasis=True,
        strikethrough=True,
        tables=True,
        safelink=True,
        escape=True,
        smartypants=True
    )
    Misaka(app, **markdown_opts)

    # user management provided by flask_login
    login_manager = LoginManager(app)
    login_manager.login_view = 'ekklesia.login'

    # XXX: for testing: just use first user from the DB as anon user
    # login_manager.anonymous_user = lambda: User.query.first()

    from ekklesia_portal.database.datamodel import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # i18n via flask-babelex
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return session["locale"]

    # OAuth2 using flask-dance
    init_oauth_ext(app)

    @app.before_request
    def set_locale():
        locale = session.get("locale")
        if locale:
            logg.debug("locale from session: %s", locale)
        else:
            locale = request.accept_languages.best_match(['de', 'en', 'fr'])
            logg.debug("locale from request: %s", locale)
            session["locale"] = locale
        g.locale = locale

    import ekklesia_portal.views
    import ekklesia_portal.views.admin

    # needed when running behind a reverse proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app
