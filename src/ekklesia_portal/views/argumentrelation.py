import logging
#from flask.ext.babelex import _
#from flask_login import current_user
#from flask_wtf import Form
#from wtforms import TextField
#from wtforms.validators import DataRequired
#import flask_sijax
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import ArgumentRelation, ArgumentVote
from ekklesia_portal.cells.argumentrelation import ArgumentRelationCell


logg = logging.getLogger(__name__)


# class ArgumentForm(Form):
#    title = TextField("headline", validators=[DataRequired()])
#    abstract = TextField("abstract", validators=[DataRequired()])
#    details = TextField("details")

@App.path(model=ArgumentRelation, path="/propositions/{proposition_id}/arguments/{argument_id}")
def argument_relation(request, proposition_id, argument_id):
    argument_relation = request.q(ArgumentRelation).filter_by(proposition_id=proposition_id, argument_id=argument_id).scalar()
    return argument_relation


@App.html(model=ArgumentRelation)
def show_argument_relation(self, request):
    return ArgumentRelationCell(self, request).show()


@App.html(model=ArgumentRelation, name='vote', request_method='POST')
def post_vote(self, request):
    vote_weight = request.POST.get('weight')
    if vote_weight not in ('-1', '0', '1'):
        raise HTTPBadRequest()

    vote = request.db_session.query(ArgumentVote).filter_by(relation=self, member=request.current_user).scalar()
    if vote is None:
        vote = ArgumentVote(relation=self, member=request.current_user, weight=int(vote_weight))
        request.db_session.add(vote)
    else:
        vote.weight = int(vote_weight)

    redirect_url = request.link(self.proposition) + '#argument_relation_' + str(self.id)
    return redirect(redirect_url)


#@app.route("/<proposition_url>/<argument_type>/new", methods=["GET", "POST"])
def new_argument_relation(proposition_url, argument_type):
    logg.debug("new argument form: %s", request.form)
    proposition = Proposition.query.filter_by(url=proposition_url).first_or_404()
    form = ArgumentForm()

    if request.method == "POST" and form.validate():
        arg = Argument(url=form.title.data.replace(" ", "-"), details=form.details.data, title=form.title.data,
                       abstract=form.abstract.data, argument_type=argument_type, proposition=proposition, author=current_user)
        db.session.add(arg)
        db.session.commit()
        return redirect(url_for("proposition", proposition_url=proposition.url))

    return render_template("new_argument.j2.jade", proposition=proposition, argument_type=argument_type)
