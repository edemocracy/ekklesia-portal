import logging
from flask import render_template, abort, request, url_for, redirect
from arguments import app, db
from arguments.database.datamodel import Question, Tag
from flask.ext.babelex import _
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


logg = logging.getLogger(__name__)


class QuestionForm(Form):
    title = TextField("title", validators=[DataRequired()])
    details = TextField("details", default="")
    tags = TextField("tags", default="")


@app.route("/<question_url>")
def question(question_url):
    question = Question.query.filter_by(url=question_url).first_or_404()
    return render_template("question.j2.jade", question=question)


@app.route("/new", methods=["GET", "POST"])
def new_question():
    logg.debug("new question form: %s", request.form)
    form = QuestionForm()

    if request.method == "POST" and form.validate():
        question = Question(url=form.title.data.replace(" ", "-"), details=form.details.data, title=form.title.data)
        
        import ipdb; ipdb.set_trace()
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

