import logging

from ekklesia_common.lid import LID
from morepath import redirect
from webob.exc import HTTPBadRequest

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Argument, ArgumentRelation, ArgumentVote, Proposition
from ekklesia_portal.enums import ArgumentType
from ekklesia_portal.permission import CreatePermission, VotePermission

from .argument_relation_cells import ArgumentRelationCell, NewArgumentForPropositionCell
from .argument_relation_contracts import ArgumentForPropositionForm
from .argument_relations import ArgumentRelations

logg = logging.getLogger(__name__)


@App.permission_rule(model=ArgumentRelations, permission=CreatePermission)
def argument_relation_create_permission(identity, model, permission):
    # All logged-in users may create new arguments.
    # We will have more restrictions in the future.
    return True


@App.permission_rule(model=ArgumentRelation, permission=VotePermission)
def argument_relation_vote_permission(identity, model, permission):
    # All logged-in users may vote on arguments.
    # We will have more restrictions in the future.
    return True


@App.path(model=ArgumentRelation, path="/p/{proposition_id}/a/{argument_id}")
def argument_relation(request, proposition_id=LID(), argument_id=0):
    argument_relation = request.q(ArgumentRelation).filter_by(
        proposition_id=proposition_id, argument_id=argument_id
    ).scalar()
    return argument_relation


@App.path(model=ArgumentRelations, path="/p/{proposition_id}/a")
def argument_relations(request, proposition_id=LID(), relation_type=None):
    return ArgumentRelations(proposition_id, relation_type)


@App.html(model=ArgumentRelation)
def show_argument_relation(self, request):
    return ArgumentRelationCell(self, request).show()


@App.html(model=ArgumentRelation, name='vote', request_method='POST', permission=VotePermission)
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


@App.html(model=ArgumentRelations, name='new', permission=CreatePermission)
def new(self, request):
    form_data = {
        'relation_type': ArgumentType[self.relation_type],
        'proposition_id': self.proposition_id,
    }
    form = ArgumentForPropositionForm(request, request.link(self))
    return NewArgumentForPropositionCell(request, form, form_data, model=self).show()


@App.html_form_post(
    model=ArgumentRelations,
    form=ArgumentForPropositionForm,
    cell=NewArgumentForPropositionCell,
    permission=CreatePermission
)
def create(self, request, appstruct):
    proposition = request.db_session.query(Proposition).get(self.proposition_id)
    if proposition is None:
        raise HTTPBadRequest()

    argument = Argument(
        title=appstruct['title'],
        abstract=appstruct['abstract'],
        details=appstruct['details'],
        author=request.current_user
    )

    argument_relation = ArgumentRelation(
        proposition=proposition, argument=argument, argument_type=appstruct['relation_type']
    )

    request.db_session.add(argument)
    request.db_session.add(argument_relation)
    request.db_session.flush()
    return redirect(request.link(proposition))
