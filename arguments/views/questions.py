#from flask import render_template, request
from arguments.app import App
#from arguments.database.datamodel import Question, Tag
from munch import Munch
from datetime import datetime


class Questions:
    def __init__(self, mode, searchterm, tag):
        self.searchterm = searchterm
        self.mode = mode
        self.tag = tag

    @property
    def questions(self):
        arguments = [Munch(title="Test", created_at=123)]
        if self.tag:
            return [Munch(name="Wat?", tags=["a", "b"])]
        else:
            return [Munch(name="Häh?", tags=["verstenix"], arguments=arguments, created_at=123)]

        questions = q(Question)

        if self.searchterm:
            questions = questions.search(self.searchterm)

        if self.tag:
            questions = questions.join(Tag, Question.tags).filter_by(tag=self.tag)

        if self.mode == "top":
            questions = questions.order_by(Question.score.desc())

        elif self.mode == "sorted":
            questions = questions.order_by(Question.url)

        elif self.mode == "custom":
            raise NotImplementedError()

        return questions


@App.path(model=Questions, path='')
def questions(q, tag, mode="sorted"):
    return Questions(mode, q, tag)


@App.html(model=Questions)
def questions_html(self, request):
    return request.app.render_template("questions.j2.jade", questions=self.questions, mode=self.mode, tag=self.tag, searchterm=self.searchterm)
