#from flask.ext.babelex import _
#from flask import render_template, abort
from arguments import app
#from arguments.database.datamodel import Question, Argument


#@app.route("/<question_url>/<argument_url>/ca")
def counter_arguments(question_url, argument_url):
    argument = (Argument.query
                .filter_by(url=argument_url)
                .join(Question)
                .filter_by(url=question_url).first_or_404())

    return render_template("counter_arguments.j2.jade", argument=argument)

