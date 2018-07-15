import logging
from deform import ValidationFailure
from morepath import redirect
from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.collections.argument_relations import ArgumentRelations
from ekklesia_portal.database.datamodel import Argument, ArgumentRelation, ArgumentVote, Proposition
from ekklesia_portal.cells.argumentrelation import ArgumentRelationCell, NewArgumentForPropositionCell


logg = logging.getLogger(__name__)


@App.path(model=ArgumentRelation, path="/propositions/{proposition_id}/arguments/{argument_id}")
def argument_relation(request, proposition_id, argument_id):
    argument_relation = request.q(ArgumentRelation).filter_by(proposition_id=proposition_id, argument_id=argument_id).scalar()
    return argument_relation


@App.path(model=ArgumentRelations, path="/propositions/{proposition_id}/arguments")
def argument_relations(request, proposition_id, relation_type=None):
    return ArgumentRelations(proposition_id, relation_type)


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


@App.html(model=ArgumentRelations, name='new')
def new(self, request):
    form_data ={
        'relation_type': self.relation_type,
        'proposition_id': self.proposition_id,
    }
    proposition = request.db_session.query(Proposition).get(self.proposition_id)
    return NewArgumentForPropositionCell(self.form(request.link(self)), request, form_data, proposition).show()


@App.html(model=ArgumentRelations, request_method='POST')
def create(self, request):
    controls = request.POST.items()
    form = self.form(request.link(self))
    proposition = request.db_session.query(Proposition).get(self.proposition_id)
    try:
        appstruct = form.validate(controls)
    except ValidationFailure as e:
        return NewArgumentForPropositionCell(form, request, None, proposition).show()

    argument = Argument(title=appstruct['title'], abstract=appstruct['abstract'], details=appstruct['details'])
    argument_relation = ArgumentRelation(proposition=proposition, argument=argument, argument_type=appstruct['relation_type'])
    request.db_session.add(argument)
    request.db_session.add(argument_relation)
    request.db_session.flush()
    return redirect(request.link(proposition))
