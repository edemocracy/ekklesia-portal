import logging
from flask import render_template, abort, request, url_for, redirect, g
from flask_login import current_user
from arguments import app, db
from arguments.database.datamodel import Question, Tag
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
import flask_sijax
from arguments.sijax_callbacks import argument_vote


logg = logging.getLogger(__name__)


class QuestionForm(Form):
    title = TextField("title", validators=[DataRequired()])
    details = TextField("details", default="")
    tags = TextField("tags", default="")


@flask_sijax.route(app, "/<question_url>")
def question(question_url):

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('argument_vote', argument_vote)
        return g.sijax.process_request()

    question = Question.query.filter_by(url=question_url).first_or_404()
    return render_template("question.j2.jade", question=question)


@app.route("/new", methods=["GET", "POST"])
def new_question():
    logg.debug("new question form: %s", request.form)
    form = QuestionForm()

    if request.method == "POST" and form.validate():
        question = Question(url=form.title.data.replace(" ", "-"), details=form.details.data, title=form.title.data)

        tags = [t.strip() for t in form.tags.data.split(",")]
        existing_tags = Tag.query.filter(Tag.tag.in_(tags)).all()
        question.tags.extend(existing_tags)
        new_tags = set(tags) - {t.tag for t in existing_tags}

        for tag_name in new_tags:
            tag = Tag(tag=tag_name)
            question.tags.append(tag)
            db.session.add(tag)

        db.session.add(question)
        db.session.commit()
        return redirect(url_for("question", question_url=question.url))

    return render_template("new_question.j2.jade")

