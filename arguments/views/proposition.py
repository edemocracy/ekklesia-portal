import logging
#from flask import render_template, abort, request, url_for, redirect, g
#from flask_login import current_user, login_required
#from flask_wtf import Form
#from wtforms import TextField
#from wtforms.validators import DataRequired
#import flask_sijax
import requests

from arguments.app import App
from arguments.database.datamodel import Proposition, Tag, Argument
from arguments.sijax_callbacks import argument_vote, proposition_vote
from arguments.helper.cell import Cell


logg = logging.getLogger(__name__)


# XXX: we support two association types, make it configurable
QUESTION_ASSOCIATION_TYPES = {
    "left": "change",
    "right": "counter",
    "": ""
}


#class PropositionForm(Form):
#    associated_with_proposition_url = TextField(default="")
#    association_type = TextField(default="")
#    title = TextField("title", validators=[DataRequired()])
#    details = TextField("details", default="")
#    tags = TextField("tags", default="")

class PropositionCell(Cell):
    model_properties = ['id', 'title', 'content', 'motivation']
    
    def new_argument_url(self, argument_type):
        return "#"
        self.class_link(Argument, dict(argument_type=argument_type), 'new')
        
    def arguments(self, argument_type):
        return []


#@flask_sijax.route(app, "/<proposition_url>")
@App.path(model=Proposition, path="/propositions/{proposition_id}")
def proposition(request, proposition_id):
    # XXX: this line should be moved to a decorator wrapping flask_sijax.route because we need this for all sijax views.
    #g.sijax.set_request_uri(request.path)

    #if g.sijax.is_sijax_request:
    #    g.sijax.register_callback('argument_vote', argument_vote)
    #    g.sijax.register_callback('proposition_vote', proposition_vote)
    #    return g.sijax.process_request()

    proposition = request.q(Proposition).get(proposition_id)
    return proposition


@App.html(model=Proposition)
def proposition_show(self, request):
    return PropositionCell(self, request).show()


#@app.route("/<proposition_url>/associated")
def proposition_associated(proposition_url):
    proposition = Proposition.query.filter_by(url=proposition_url).first_or_404()
    associated_propositions_left = proposition.associated_propositions(QUESTION_ASSOCIATION_TYPES["left"])
    associated_propositions_right = proposition.associated_propositions(QUESTION_ASSOCIATION_TYPES["right"])

    return render_template("proposition_associated.j2.jade",
            proposition=proposition,
            associated_propositions_left=associated_propositions_left,
            associated_propositions_right=associated_propositions_right)


def _handle_post_new_proposition(form):
    proposition = Proposition(url=form.title.data.replace(" ", "-"),
                        details=form.details.data,
                        title=form.title.data)

    associated_with_proposition_url = form.associated_with_proposition_url.data
    if associated_with_proposition_url:
        associated_with_proposition = Proposition.query.filter_by(url=associated_with_proposition_url).scalar()
        qrel = PropositionAssociation(left=associated_with_proposition,
                right=proposition, association_type=form.association_type.data)
        db.session.add(qrel)

    tags = [t.strip() for t in form.tags.data.split(",") if t.strip()]
    existing_tags = Tag.query.filter(Tag.tag.in_(tags)).all()
    proposition.tags.extend(existing_tags)
    new_tags = set(tags) - {t.tag for t in existing_tags}

    for tag_name in new_tags:
        tag = Tag(tag=tag_name)
        proposition.tags.append(tag)
        db.session.add(tag)

    db.session.add(proposition)
    db.session.commit()
    return redirect(url_for("proposition", proposition_url=proposition.url))


def _import_discourse_post(base_url, from_data):
    post_id = int(from_data)
    post_url = "{}/posts/{}".format(base_url, post_id)

    res = requests.get(post_url, headers=dict(Accept="application/json"))
    content = res.json()

    details = content.get("raw")
    if details is None:
        raise ValueError("malformed discourse post JSON, key 'raw' not found!")

    topic_id = content.get("topic_id")
    if topic_id is None:
        raise ValueError("malformed discourse post JSON, key 'raw' not found!")

    topic_url = "{}/t/{}".format(base_url, topic_id)
    res = requests.get(topic_url, headers=dict(Accept="application/json"))
    content = res.json()

    title = content.get("title")
    if title is None:
        raise ValueError("malformed discourse topic JSON, key 'title' not found!")

    return title, details, None


QUESTION_IMPORT_HANDLERS = {
    "discourse_post": _import_discourse_post
}


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

    from_data = request.args.get("from_data")
    source = request.args.get("source")

    if from_data and source:
        # pre-fill new proposition form from a URL return data formatted as `from_format`
        # 'for supported formats, see 'QUESTION_IMPORT_HANDLERS'
        import_info = app.config["QUESTION_SOURCES"].get(source)

        if import_info is None:
            raise ValueError("unsupported proposition source: " + source)

        from_format, base_url = import_info
        
        import_handler = QUESTION_IMPORT_HANDLERS.get(from_format)
        if import_handler is None:
            raise ValueError("unsupported proposition import format: " + from_format)
        
        imp_title, imp_details, imp_tags = import_handler(base_url, from_data)

        if imp_title is not None:
            title = imp_title
        if imp_details is not None:
            details = imp_details
        if imp_tags is not None:
            tags = imp_tags

    return render_template("new_proposition.j2.jade",
            associated_with_proposition_url=associated_with_proposition_url,
            association_type=association_type,
            title=title,
            details=details,
            tags=",".join(tags))

