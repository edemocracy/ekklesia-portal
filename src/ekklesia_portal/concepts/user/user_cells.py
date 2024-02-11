from ekklesia_common.cell import Cell
from ekklesia_common.permission import EditPermission

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.proposition import Propositions
from ekklesia_portal.concepts.user.user_helper import items_for_user_select_widgets
from ekklesia_portal.datamodel import Group, User, UserProfile, SubjectArea
from ekklesia_portal.enums import PropositionStatus, SupporterStatus


@App.cell()
class UserCell(LayoutCell):

    _model: User
    model_properties = ['name', 'joined', 'profile', 'departments', 'areas', 'groups', 'last_active']

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)

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

    def supported_areas(self):
        return [
            support.proposition.ballot.area for support in self._model.member_propositions
            if support.status == SupporterStatus.ACTIVE and support.proposition.status == PropositionStatus.SUBMITTED
        ]

    def supported_link(self, subject_area: SubjectArea):
        return self.class_link(
            Propositions, {
                "department": subject_area.department.name,
                "subject_area": subject_area.name,
                "only_supporting": "yes"
            }
        )


@App.cell('edit')
class EditUserCell(EditFormCell):

    _model: User

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        form_data['groups'] = [g.name for g in self._model.groups]
        self.set_form_data(form_data)
        groups = self._request.q(Group)
        items = items_for_user_select_widgets(groups)
        self._form.prepare_for_render(items)


@App.cell()
class UserProfileCell(Cell):

    _model: UserProfile
    model_properties = ['sub', 'eligible', 'verified', 'roles', 'profile']
