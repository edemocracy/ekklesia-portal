from ekklesia_common.identity_policy import NoIdentity

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import Department
from ekklesia_portal.concepts.proposition import Propositions
from ekklesia_portal.permission import CreatePermission, EditPermission

from .departments import Departments
from ...enums import VotingStatus


@App.cell(Departments)
class DepartmentsCell(LayoutCell):

    def departments(self):
        return list(self._model.departments(self._request.q))

    def my_departments(self):
        if self.current_user is None:
            return []
        return self.current_user.departments

    def other_departments(self):
        if self.current_user is None:
            return []
        return [d for d in self.departments if d not in self.my_departments]

    def is_global_admin(self):
        if self.current_user is None:
            return False
        return self._request.identity.has_global_admin_permissions

    def show_new_button(self):
        return self.options.get('show_new_button'
                                ) and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(Department)
class DepartmentCell(LayoutCell):

    model_properties = ['areas', 'description', 'name', 'voting_phases']

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)

    def proposition_count(self):
        if type(self._request.identity) is NoIdentity:
            return Propositions(department=self._model.name, status="submitted,qualified,scheduled,voting"). \
                propositions(self._request.q, False, count=True)
        return Propositions(department=self._model.name, status="submitted,qualified,scheduled,voting").\
            propositions(self._request.q, self._request.identity.has_global_admin_permissions, count=True)

    def draft_count(self):
        if type(self._request.identity) is NoIdentity:
            return Propositions(department=self._model.name, status="draft"). \
                propositions(self._request.q, False, count=True)
        return Propositions(department=self._model.name, status="draft"). \
            propositions(self._request.q, self._request.identity.has_global_admin_permissions, count=True)

    def department_propositions_url(self):
        return self.class_link(Propositions, dict(status="submitted,qualified,scheduled,voting", department=self._model.name))

    def department_drafts_url(self):
        return self.class_link(Propositions, dict(status="draft", department=self._model.name))

    def active_voting_phases(self):
        voting_phases = []
        for voting_phase in self._model.voting_phases:
            if voting_phase.status in [VotingStatus.PREPARING, VotingStatus.VOTING]:
                title = voting_phase.title
                voting_phases.append((title, self.link(voting_phase)))
        return voting_phases

    def member_count(self):
        return len(self._model.members)


class NewDepartmentCell(NewFormCell):
    pass


class EditDepartmentCell(EditFormCell):
    pass
