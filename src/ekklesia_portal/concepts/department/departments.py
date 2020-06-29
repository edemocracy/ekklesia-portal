from ekklesia_portal.datamodel import Department


class Departments:

    def departments(self, q):
        query = q(Department)
        return query.all()
