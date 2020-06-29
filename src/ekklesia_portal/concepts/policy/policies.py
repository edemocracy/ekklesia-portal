from ekklesia_portal.datamodel import Policy


class Policies:

    def policies(self, q):
        query = q(Policy)
        return query.all()
