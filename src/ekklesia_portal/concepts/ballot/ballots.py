from ekklesia_portal.datamodel import Ballot

from .ballot_contracts import BallotForm


class Ballots:

    def __init__(self, department=None):
        self.department = department

    def ballots(self, q):
        query = q(Ballot)

        if self.department is None:
            return query

        return query.filter(department_id=self.department)

    def form(self, action, request):
        return BallotForm(request, action)
