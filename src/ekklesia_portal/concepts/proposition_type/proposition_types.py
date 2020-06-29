from ekklesia_portal.datamodel import PropositionType


class PropositionTypes:

    def proposition_types(self, q):
        query = q(PropositionType)
        return query.all()
