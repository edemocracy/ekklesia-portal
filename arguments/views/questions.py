from flask import render_template, request
from arguments import app
from arguments.database.datamodel import Question, Tag


@app.route("/")
@app.route("/tags/<tag>")
def questions(tag=None):
    questions = Question.query
    mode = request.args.get("mode")
    searchterm = request.args.get("q")
    #import ipdb; ipdb.set_trace()

    if searchterm:
        questions = questions.search(searchterm)

    if tag:
        questions = questions.join(Tag, Question.tags).filter_by(tag=tag)

    if mode == "top":
        questions = questions.order_by(Question.score.desc())

    elif mode is None or mode == "sorted":
        questions = questions.order_by(Question.url)

    elif mode == "custom":
        raise NotImplementedError()

    return render_template("questions.j2.jade", questions=questions, mode=mode, tag=tag, searchterm=searchterm)

