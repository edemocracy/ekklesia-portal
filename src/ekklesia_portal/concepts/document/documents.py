from ekklesia_portal.datamodel import Document


class Documents:

    def documents(self, q):
        query = q(Document)
        return query.all()
