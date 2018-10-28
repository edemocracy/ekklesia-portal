from ekklesia_portal.database.datamodel import Policy


class Policies:

    def policies(self, q):
        query = q(Policy)
        return query.all()
