import logging
from flask import render_template, abort, request, url_for, redirect, g
from flask_login import current_user
from arguments import app, db
from arguments.database.datamodel import Question, Tag, QuestionAssociation
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
import flask_sijax
from arguments.sijax_callbacks import argument_vote, question_vote


logg = logging.getLogger(__name__)


class QuestionForm(Form):
    associated_with_question_url = TextField(default="")
    association_type = TextField(default="")
    title = TextField("title", validators=[DataRequired()])
    details = TextField("details", default="")
    tags = TextField("tags", default="")


@flask_sijax.route(app, "/<question_url>")
def question(question_url):

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('argument_vote', argument_vote)
        g.sijax.register_callback('question_vote', question_vote)
        return g.sijax.process_request()

    question = Question.query.filter_by(url=question_url).first_or_404()
    return render_template("question.j2.jade", question=question)


@app.route("/<question_url>/associated")
def question_associated(question_url):
    question = Question.query.filter_by(url=question_url).first_or_404()
    return render_template("question_associated.j2.jade", question=question)


@app.route("/<associated_with_question_url>/associated/<association_type>/new", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def new_question(associated_with_question_url="", association_type=""):
    logg.debug("new question form: %s", request.form)
    form = QuestionForm()

    if request.method == "POST" and form.validate():
        question = Question(url=form.title.data.replace(" ", "-"),
                            details=form.details.data,
                            title=form.title.data)

        associated_with_question_url = form.associated_with_question_url.data
        if associated_with_question_url is not None:
            associated_with_question = Question.query.filter_by(url=associated_with_question_url).scalar()
            qrel = QuestionAssociation(left=associated_with_question, 
                    right=question, association_type=form.association_type.data)
            db.session.add(qrel)

        tags = [t.strip() for t in form.tags.data.split(",") if t.strip()]
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

    return render_template("new_question.j2.jade", 
            associated_with_question_url=associated_with_question_url, 
            association_type=association_type)

