import logging
#from flask.ext.babelex import _
#from flask_login import current_user
#from flask_wtf import Form
#from wtforms import TextField
#from wtforms.validators import DataRequired
#import flask_sijax
from arguments.app import App
from arguments.database.datamodel import Argument
from arguments.cells.argument import ArgumentCell


logg = logging.getLogger(__name__)


# class ArgumentForm(Form):
#    title = TextField("headline", validators=[DataRequired()])
#    abstract = TextField("abstract", validators=[DataRequired()])
#    details = TextField("details")

@App.path(model=Argument, path="/arguments/{id}")
def argument(request, id):
    argument = request.q(Argument).get(id)
    return argument


@App.html(model=Argument)
def show_argument(self, request):
    return ArgumentCell(self, request, extended=True).show()


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
