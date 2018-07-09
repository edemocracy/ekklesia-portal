import logging
#from flask import render_template, abort, request, url_for, redirect, g
#from flask_login import current_user, login_required
#from flask_wtf import Form
#from wtforms import TextField
#from wtforms.validators import DataRequired
import requests

from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Proposition
from ekklesia_portal.cells.proposition import PropositionCell


logg = logging.getLogger(__name__)


# class PropositionForm(Form):
#    associated_with_proposition_url = TextField(default="")
#    association_type = TextField(default="")
#    title = TextField("title", validators=[DataRequired()])
#    details = TextField("details", default="")
#    tags = TextField("tags", default="")


@App.path(model=Proposition, path="/propositions/{proposition_id}", variables=lambda o: dict(proposition_id=o.id))
def proposition(request, proposition_id):
    proposition = request.q(Proposition).get(proposition_id)
    return proposition


@App.html(model=Proposition)
def proposition_show(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='discussion')
    return cell.show()


@App.html(model=Proposition, name='associated')
def proposition_show_associated(self, request):
    cell = PropositionCell(self, request, show_tabs=True, show_details=True, show_actions=True, active_tab='associated')
    return cell.show()

#@app.route("/<associated_with_proposition_url>/associated/<side>/new", methods=["GET", "POST"])
#@app.route("/new", methods=["GET", "POST"])
#@app.route("/propositions/new", methods=["GET", "POST"])
#@login_required
def new_proposition(associated_with_proposition_url="", side=""):
    logg.debug("new proposition form: %s", request.form)

    form = PropositionForm()

    if request.method == "POST" and form.validate():
        return _handle_post_new_proposition(form)

    association_type = QUESTION_ASSOCIATION_TYPES[side]

    # pre-fill new proposition form from URL params if given
    title = request.args.get("title", "")
    details = request.args.get("details", "")
    tags = request.args.getlist("tags")

    return render_template("new_proposition.j2.jade",
                           associated_with_proposition_url=associated_with_proposition_url,
                           association_type=association_type,
                           title=title,
                           details=details,
                           tags=",".join(tags))
