#from flask.ext.babelex import _
#from flask import render_template, abort
from ekklesia_portal import app
#from ekklesia_portal.database.datamodel import Proposition, Argument


#@app.route("/<proposition_url>/<argument_url>/ca")
def counter_arguments(proposition_url, argument_url):
    argument = (Argument.query
                .filter_by(url=argument_url)
                .join(Proposition)
                .filter_by(url=proposition_url).first_or_404())

    return render_template("counter_arguments.j2.jade", argument=argument)

