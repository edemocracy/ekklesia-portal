from uuid import UUID, uuid5
from morepath import redirect
import deform
from eliot import start_action, Message
#from webob.exc import HTTPBadRequest
from ekklesia_portal.app import App
from ekklesia_portal.database.datamodel import BallotVoting, Vote, VoteToken
from ekklesia_portal.permission import WritePermission
from .ballot_voting_cells import BallotVotingCell, BallotVotingVoteCell, BallotVotingConfirmCell, BallotVotingsCell
from .ballot_voting_contracts import ballot_voting_form
from .ballot_votings import BallotVotings


class VotePermission(WritePermission):
    pass


@App.permission_rule(model=BallotVoting, permission=VotePermission)
def ballot_voting_permission(identity, model, permission):
    return True


@App.permission_rule(model=BallotVotings, permission=VotePermission)
def ballot_votings_permission(identity, model, permission):
    return True


@App.path(model=BallotVotings, path='ballot_votings')
def ballot_votings():
    return BallotVotings()


@App.path(model=BallotVoting, path='ballot_votings/{uuid}')
def ballot_voting(request, uuid):
    return request.q(BallotVoting).get(uuid)


@App.html(model=BallotVotings, permission=VotePermission)
def index(self, request):
    cell = BallotVotingsCell(self, request)
    return cell.show()


@App.html(model=BallotVoting, permission=VotePermission)
def show(self, request):
    cell = BallotVotingCell(self, request)
    return cell.show()


@App.html(model=BallotVoting, name='confirm', permission=VotePermission)
def confirm(self, request):
    cell = BallotVotingConfirmCell(self, request)
    return cell.show()


@App.html(model=BallotVoting, name='confirm', request_method='POST', permission=VotePermission)
def confirm_post(self, request):
    auid = request.browser_session['auid']
    confirmed_token = request.POST.getall('token')
    votes_to_confirm = (request.q(Vote)
                               .join(VoteToken)
                               .filter(VoteToken.auid == auid, VoteToken.token.in_(confirmed_token)))

    for vote in votes_to_confirm:
        vote.confirmed = True

    token_str = ','.join(confirmed_token)

    return f"stimme gezählt für Token {token_str}, danke..."


@App.html(model=BallotVoting, name='vote', permission=VotePermission)
def vote(self, request):
    cell = BallotVotingVoteCell(self, request)
    return cell.show()


@App.html(model=BallotVoting, name='vote', request_method='POST', permission=VotePermission)
def vote_post(self, request):

    form = ballot_voting_form(self, request)
    controls = list(request.POST.items())
    with start_action(action_type='validate_form',
                      controls=dict(c for c in controls if not c[0].startswith('_')),
                      form=form) as action:
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure:
            Message.log(validation_errors=form.error.asdict())
            if request.app.settings.app.fail_on_form_validation_error:
                raise form.error
            return

        action.add_success_fields(appstruct=appstruct)

        namespace_uuid = UUID('36052f9a-e24f-4de0-a8c3-4cbac06608d6')
        auid = uuid5(namespace_uuid, request.current_user.name)
        request.browser_session['auid'] = str(auid)

        for option in self.options:
            result = appstruct[str(option.uuid)]
            vote = Vote(yes_no=result['yes_no'], points=result['points'], option=option)
            vote_token = VoteToken(auid=auid, vote=vote)
            request.db_session.add(vote_token)

    return redirect(request.link(self, 'confirm'))
