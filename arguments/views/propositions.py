#from flask import render_template, request
from arguments.app import App
from arguments.database.datamodel import Proposition, Tag
from munch import Munch
from datetime import datetime


class Propositions:
    def __init__(self, mode, searchterm, tag):
        self.searchterm = searchterm
        self.mode = mode
        self.tag = tag

    def propositions(self, q):
        propositions = q(Proposition)

        if self.searchterm:
            propositions = propositions.search(self.searchterm)

        if self.tag:
            propositions = propositions.join(Tag, Proposition.tags).filter_by(tag=self.tag)

        if self.mode == "top":
            propositions = propositions.order_by(Proposition.score.desc())

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions


@App.path(model=Propositions, path='')
def propositions(request, q, tag, mode="sorted"):
    return Propositions(mode, q, tag)


@App.html(model=Propositions)
def propositions_html(self, request):
    q = request.q
    propositions = self.propositions(q)
    return request.app.render_template("propositions.j2.jade", propositions=propositions, mode=self.mode, tag=self.tag, searchterm=self.searchterm)
