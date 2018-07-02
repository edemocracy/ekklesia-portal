from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import Proposition, Tag
from ekklesia_portal.cells.propositions import PropositionsCell
from ekklesia_portal.cells.proposition import NewPropositionCell
from ekklesia_portal.collections.propositions import Propositions


@App.path(model=Propositions, path='propositions')
def propositions(request, searchterm=None, tag=None, mode="sorted"):
    return Propositions(mode, searchterm, tag)


@App.html(model=Propositions)
def propositions_html(self, request):
    return PropositionsCell(self, request).show()


@App.html(model=Propositions, name='new')
def new(self, request):
    return NewPropositionCell(self.form(request.class_link(Propositions)), request, {}).show()


@App.html(model=Propositions, request_method='POST')
def proposition_create(self, request):
    controls = request.POST.items()
    form = self.form(request.class_link(Propositions))
    try:
        appstruct = form.validate(controls)
    except ValidationFailure as e:
        return NewPropositionCell(form, request).show()

    tag_names = appstruct['tags']
    tags = request.db_session.query(Tag).filter(Tag.name.in_(tag_names)).all()

    new_tag_names = set(tag_names) - {t.name for t in tags}

    for tag_name in new_tag_names:
        tag = Tag(name=tag_name)
        tags.append(tag)

    appstruct['tags'] = tags

    relation_type = appstruct.pop('relation_type')
    related_proposition_id = appstruct.pop('related_proposition_id')
    if relation_type and related_proposition_id:
        related_proposition = request.db_session.query(Proposition).get(related_proposition_id)
        if related_proposition is None:
            raise HTTPBadRequest()

        if relation_type == 'modifies':
            appstruct['modifies'] = related_proposition
        elif relation_type == 'replaces':
            appstruct['replaces'] = related_proposition

    proposition = Proposition(**appstruct)
    request.db_session.add(proposition)
    request.db_session.flush()

    return redirect(request.link(proposition))
