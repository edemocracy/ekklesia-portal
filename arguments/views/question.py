from flask import render_template, abort
from arguments import app
from arguments.database.datamodel import Question


@app.route("/<question_url>")
def question(question_url):
    question = Question.query.filter_by(url=question_url).first_or_404()
    return render_template("question.j2.jade", question=question)
