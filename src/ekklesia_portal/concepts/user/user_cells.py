from ekklesia_common.cell import Cell

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import User, UserProfile, AreaMember, SubjectArea
from ekklesia_portal.enums import EkklesiaUserType


@App.cell(User)
class UserCell(LayoutCell):
    model_properties = ['name', 'joined', 'profile', 'departments', 'areas', 'groups', 'last_active']

    def departments_with_subject_areas(self):
        department_to_areas = {d: [] for d in self._model.departments}
        member_area_set = set()
        for i in self._model.member_areas:
            member_area_set.add(i.area_id)
        for dep in self._model.departments:
            for area in dep.areas:
                department_to_areas[area.department].append((area, area.id in member_area_set))

        return department_to_areas.items()

    def supported_proposition_count(self):
        return len(self._model.supports)

    def argument_count(self):
        return len(self._model.supports)

    def member_area_action(self):
        return self.link(self._model, name='member_area')


@App.cell(UserProfile)
class UserProfileCell(Cell):
    model_properties = ['sub', 'eligible', 'verified', 'roles', 'profile']
