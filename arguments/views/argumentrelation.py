import logging
#from flask.ext.babelex import _
#from flask_login import current_user
#from flask_wtf import Form
#from wtforms import TextField
#from wtforms.validators import DataRequired
#import flask_sijax
from arguments.app import App
from arguments.database.datamodel import ArgumentRelation
from arguments.helper.cell import Cell


logg = logging.getLogger(__name__)


# class ArgumentForm(Form):
#    title = TextField("headline", validators=[DataRequired()])
#    abstract = TextField("abstract", validators=[DataRequired()])
#    details = TextField("details")

class ArgumentRelationCell(Cell):
    model_properties = ['proposition', 'argument']

    @property
    def proposition_url(self):
        return self.link(self._model.proposition)

    @property
    def argument_url(self):
        return self.link(self._model.argument)

    @property
    def proposition_title(self):
        return self.proposition.title

    @property
    def argument_title(self):
        return self.argument.title


@App.path(model=ArgumentRelation, path="/propositions/{id}/arguments/{argument_id}")
def argument_relation(request, id, argument_id):
    argument_relation = request.q(ArgumentRelation).filter_by(proposition_id=id, argument_id=argument_id).scalar()
    return argument_relation


@App.html(model=ArgumentRelation)
def show_argument_relation(self, request):
    return ArgumentRelationCell(self, request).show()


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
