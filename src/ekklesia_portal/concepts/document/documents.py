from ekklesia_portal.database.datamodel import Document


class Documents:

    def documents(self, q):
        query = q(Document)
        return query.all()
