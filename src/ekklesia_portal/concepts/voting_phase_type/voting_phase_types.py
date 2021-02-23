from ekklesia_portal.datamodel import VotingPhaseType


class VotingPhaseTypes:

    def voting_phase_types(self, q):
        query = q(VotingPhaseType)
        return query.all()
