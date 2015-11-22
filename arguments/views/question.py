import logging
from flask import render_template, abort, request, url_for, redirect, g
from flask_login import current_user
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
import flask_sijax
import requests

from arguments import app, db
from arguments.database.datamodel import Question, Tag, QuestionAssociation
from arguments.sijax_callbacks import argument_vote, question_vote


logg = logging.getLogger(__name__)


# XXX: we support two association types, make it configurable
QUESTION_ASSOCIATION_TYPES = {
    "left": "change",
    "right": "counter",
    "": ""
}


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
    associated_questions_left = question.associated_questions(QUESTION_ASSOCIATION_TYPES["left"])
    associated_questions_right = question.associated_questions(QUESTION_ASSOCIATION_TYPES["right"])

    return render_template("question_associated.j2.jade", 
            question=question,
            associated_questions_left=associated_questions_left,
            associated_questions_right=associated_questions_right)


def _handle_post_new_question(form):
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


def _import_discourse_post(from_url):
    res = requests.get(from_url, headers=dict(Accept="application/json"))
    content = res.json()
    details = content.get("raw")
    if details is None:
        raise ValueError("malformed discourse post JSON, key 'raw' not found!")

    return None, details, None


QUESTION_IMPORT_HANDLERS = {
        "discourse_post": _import_discourse_post
}


@app.route("/<associated_with_question_url>/associated/<association_type>/new", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
@app.route("/questions/new", methods=["GET", "POST"])
def new_question(associated_with_question_url="", side=""):
    logg.debug("new question form: %s", request.form)

    form = QuestionForm()

    if request.method == "POST" and form.validate():
        return _handle_post_new_question(form)
    

    association_type = QUESTION_ASSOCIATION_TYPES[side]

    # pre-fill new question form from URL params if given
    title = request.args.get("title", "")
    details = request.args.get("details", "")
    tags = request.args.getlist("tags")

    from_url = request.args.get("from_url")
    from_format = request.args.get("from_format")

    if from_url and from_format:
        # pre-fill new question form from a URL return data formatted as `from_format`
        #'for supported formats, see 'QUESTION_IMPORT_HANDLERS'
        import_handler = QUESTION_IMPORT_HANDLERS.get(from_format)
        if import_handler is None:
            raise ValueError("unsupported question import format: " + from_format)
        imp_title, imp_details, imp_tags = import_handler(from_url)

        if imp_title is not None:
            title = imp_title
        if imp_details is not None:
            details = imp_details
        if imp_tags is not None:
            tags = imp_tags

    return render_template("new_question.j2.jade", 
            associated_with_question_url=associated_with_question_url, 
            association_type=association_type,
            title=title,
            details=details,
            tags=",".join(tags))

