from ekklesia_portal.datamodel import VotingPhase


class VotingPhases:

    def __init__(self, department=None):
        self.department = department

    def voting_phases(self, q):
        query = q(VotingPhase)

        if self.department is None:
            return query

        return query.filter(department_id=self.department)
