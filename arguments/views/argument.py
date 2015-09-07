from flask import render_template, abort
from arguments import app
from arguments.database.datamodel import Question, Argument
from flask.ext.babelex import _


@app.route("/<question_url>/<argument_url>")
def argument(question_url, argument_url):
    argument = (Argument.query
                .filter_by(url=argument_url)
                .join(Question)
                .filter_by(url=question_url).first_or_404())

    return render_template("argument.j2.jade", argument=argument)

