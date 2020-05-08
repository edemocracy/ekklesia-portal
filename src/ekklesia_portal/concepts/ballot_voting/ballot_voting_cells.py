from uuid import UUID
from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.database.datamodel import BallotVoting
from .ballot_voting_contracts import ballot_voting_form
from .ballot_votings import BallotVotings


@App.cell(BallotVotings)
class BallotVotingsCell(LayoutCell):

    def ballot_votings(self):
        return list(self._model.ballot_votings(self._request.q))


@App.cell(BallotVoting)
class BallotVotingCell(LayoutCell):

    model_properties = ['ends_at', 'starts_at', 'title']

    def vote_url(self):
        return self.link(self._model, 'vote')


@App.cell(BallotVoting, 'vote')
class BallotVotingVoteCell(LayoutCell):

    model_properties = ['ends_at', 'starts_at', 'title']

    def form_html(self):
        form = ballot_voting_form(self._model, self._request)
        form_html = form.render()
        return self.markup_class(form_html)


@App.cell(BallotVoting, 'confirm')
class BallotVotingConfirmCell(LayoutCell):

    model_properties = ['title']

    def confirm_action(self):
        return self.link(self._model, 'confirm')

    def votes_to_confirm(self):

        def ee(token, vote, option):
            return {
                'token': token,
                'yes_no': vote.yes_no,
                'points': vote.points,
                'title': option.title
            }

        auid = self._request.browser_session['auid']
        votes = [ee(*t) for t in self._model.votes_to_confirm(auid)]
        return votes
