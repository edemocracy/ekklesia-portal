import logging
from flask import render_template, abort, request, redirect, url_for
from arguments import app, db
from arguments.database.datamodel import Question, Argument, User
from flask.ext.babelex import _
from flask_login import current_user
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


logg = logging.getLogger(__name__)


class ArgumentForm(Form):
    title = TextField("headline", validators=[DataRequired()])
    abstract = TextField("abstract", validators=[DataRequired()])
    details = TextField("details")


@app.route("/<question_url>/<argument_url>")
def argument(question_url, argument_url):
    argument = (Argument.query
                .filter_by(url=argument_url)
                .join(Question)
                .filter_by(url=question_url).first_or_404())

    return render_template("argument.j2.jade", argument=argument)


@app.route("/<question_url>/<argument_type>/new", methods=["GET", "POST"])
def new_argument(question_url, argument_type):
    logg.debug("new argument form: %s", request.form)
    question = Question.query.filter_by(url=question_url).first_or_404()
    form = ArgumentForm()

    if request.method == "POST" and form.validate():
        arg = Argument(url=form.title.data.replace(" ", "-"), details=form.details.data, title=form.title.data, 
                       abstract=form.abstract.data, argument_type=argument_type, question=question, author=current_user)
        db.session.add(arg)
        db.session.commit()
        return redirect(url_for("question", question_url=question.url))

    return render_template("new_argument.j2.jade", question=question, argument_type=argument_type)


