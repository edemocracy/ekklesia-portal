#from flask import render_template, request
from arguments.app import App
from arguments.database.datamodel import Proposition, Tag
from munch import Munch
from datetime import datetime


class Questions:
    def __init__(self, mode, searchterm, tag):
        self.searchterm = searchterm
        self.mode = mode
        self.tag = tag

    def questions(self, q):
        questions = q(Proposition)

        if self.searchterm:
            questions = questions.search(self.searchterm)

        if self.tag:
            questions = questions.join(Tag, Proposition.tags).filter_by(tag=self.tag)

        if self.mode == "top":
            questions = questions.order_by(Proposition.score.desc())

        elif self.mode == "sorted":
            questions = questions.order_by(Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return questions


@App.path(model=Questions, path='')
def questions(request, q, tag, mode="sorted"):
    return Questions(mode, q, tag)


@App.html(model=Questions)
def questions_html(self, request):
    q = request.q
    questions = self.questions(q)
    return request.app.render_template("questions.j2.jade", questions=questions, mode=self.mode, tag=self.tag, searchterm=self.searchterm)
