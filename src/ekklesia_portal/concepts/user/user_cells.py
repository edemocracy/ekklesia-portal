from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.enums import EkklesiaUserType
from ekklesia_portal.database.datamodel import User, UserProfile


class UserCell(LayoutCell):
    model = User
    model_properties = ['name', 'joined', 'profile', 'departments', 'areas', 'groups', 'last_active']

    def departments_with_subject_areas(self):
        department_to_areas = { d: [] for d in self._model.departments }
        for area in self._model.areas:
            department_to_areas[area.department].append(area)

        return department_to_areas.items()

    def supported_proposition_count(self):
        return len(self._model.supports)

    def argument_count(self):
        return len(self._model.supports)


class UserProfileCell(Cell):
    model = UserProfile
    model_properties = ['auid', 'profile', 'verified', 'user_type']

    def eligible_to_vote(self):
        return self._model.user_type == EkklesiaUserType.ELIGIBLE_MEMBER
