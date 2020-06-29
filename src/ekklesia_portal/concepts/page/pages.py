from ekklesia_portal.datamodel import Page


class Pages:

    def pages(self, q):
        query = q(Page)
        return query.all()
