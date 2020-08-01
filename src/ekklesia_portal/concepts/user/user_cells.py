from ekklesia_common.cell import Cell

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import User, UserProfile
from ekklesia_portal.enums import EkklesiaUserType


@App.cell(User)
class UserCell(LayoutCell):
    model_properties = ['name', 'joined', 'profile', 'departments', 'areas', 'groups', 'last_active']

    def departments_with_subject_areas(self):
        department_to_areas = {d: [] for d in self._model.departments}
        for area in self._model.areas:
            department_to_areas[area.department].append(area)

        return department_to_areas.items()

    def supported_proposition_count(self):
        return len(self._model.supports)

    def argument_count(self):
        return len(self._model.supports)


@App.cell(UserProfile)
class UserProfileCell(Cell):
    model_properties = ['sub', 'eligible', 'verified', 'roles', 'profile']
