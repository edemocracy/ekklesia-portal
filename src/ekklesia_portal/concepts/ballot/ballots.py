from ekklesia_portal.datamodel import Ballot, VotingPhase, Department

from .ballot_contracts import BallotForm


class Ballots:

    def __init__(self, department=None, voting_phase=None):
        self.department = department
        self.voting_phase = voting_phase

    def ballots(self, q):
        query = q(Ballot)

        if self.department:
            query = query.join(Department)
            query = query.filter_by(name=self.department)

        if self.voting_phase:
            query = query.join(VotingPhase)
            query = query.filter_by(name=self.voting_phase)

        return query

    def form(self, action, request):
        return BallotForm(request, action)
