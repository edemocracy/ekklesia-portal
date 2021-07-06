from ekklesia_portal.datamodel import SubjectArea


class SubjectAreas:

    def subject_areas(self, q):
        query = q(SubjectArea)
        return query.all()
