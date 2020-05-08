from ekklesia_portal.database.datamodel import BallotVoting


class BallotVotings:

    def ballot_votings(self, q):
        query = q(BallotVoting)
        return query.all()
