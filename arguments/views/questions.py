from flask import render_template, request
from arguments import app
from arguments.database.datamodel import Question


@app.route("/")
def questions():
    questions = Question.query
    mode = request.args.get("mode", "sorted")

    if mode == "top":
        questions = questions.order_by(Question.score.desc())

    elif mode == "sorted" :
        questions = questions.order_by(Question.url)

    elif mode == "custom" :
        raise NotImplementedError()

    return render_template("questions.j2.jade", questions=questions, mode=mode)
