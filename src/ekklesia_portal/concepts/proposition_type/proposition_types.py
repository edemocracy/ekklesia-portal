from ekklesia_portal.database.datamodel import PropositionType


class PropositionTypes:

    def proposition_types(self, q):
        query = q(PropositionType)
        return query.all()
