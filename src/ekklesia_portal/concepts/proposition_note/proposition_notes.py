from ekklesia_portal.datamodel import PropositionNote


class PropositionNotes:

    def proposition_notes(self, q):
        query = q(PropositionNote)
        return query.all()
