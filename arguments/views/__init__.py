"""
All view modules must be imported here.
"""

import logging
from flask import render_template, flash
from arguments import app


logg = logging.getLogger(__name__)


@app.route("/test")
def test():
    flash("wiß Ünicöde ä")
    flash("warning", "warning")
    flash("error", "error")
    return render_template("test.j2.jade")


# import all view functions defined is this package to register them with the app
from . import question
from . import questions
from . import argument
from . import counter_arguments
from . import logout
from . import sijaxcommon
