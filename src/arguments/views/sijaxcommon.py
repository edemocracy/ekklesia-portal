import logging
#from flask import g, session, render_template
#import flask_sijax
from arguments import app
from arguments.sijax_callbacks import change_locale

logg = logging.getLogger(__name__)


#@flask_sijax.route(app, "/")
def sijax_root():
    """Runs default sijax handlers which can be called from every page.
    They are defined in add_common_sijax_callbacks()."""
    if g.sijax.is_sijax_request:
        return g.sijax.process_request()


#@app.before_request
def add_common_sijax_callbacks():
    g.sijax.register_callback("change_locale", change_locale)
