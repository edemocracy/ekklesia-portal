from ekklesia_common.permission import EditPermission, ViewPermission
from ekklesia_portal.enums import PropositionStatus, SupporterStatus
from morepath.view import redirect
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Ballot, Group, Proposition, Supporter, User, AreaMember, SubjectArea

from .user_cells import EditUserCell, UserCell
from .user_contracts import UserForm


@App.permission_rule(model=User, permission=ViewPermission)
def user_view_permission(identity, model, permission):
    # XXX identity.user is detached, must compare ids instead of objects
    return identity.has_global_admin_permissions or identity.user.id == model.id


@App.permission_rule(model=User, permission=EditPermission)
def user_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=User, path='/u/{name}')
def user(request, name):
    user = request.q(User).filter_by(name=name).scalar()
    return user


@App.html(model=User, permission=ViewPermission)
def show(self, request):
    cell = UserCell(self, request, show_edit_button=True)
    return cell.show()


@App.html(model=User, name='edit', permission=EditPermission)
def edit(self, request):
    form = UserForm(request, request.link(self))
    return EditUserCell(self, request, form).show()


@App.html_form_post(model=User, form=UserForm, cell=EditUserCell, permission=EditPermission)
def update(self, request, appstruct):
    appstruct['groups'] = request.db_session.query(Group).filter(Group.name.in_(appstruct['groups'])).all()
    self.update(**appstruct)
    return redirect(request.link(self))


@App.html(model=User, name="member_area", request_method='POST', permission=ViewPermission)
def show_member_area(self, request):
    button_value = request.params['member_in_area']
    button_area_id = request.params['area_id']

    area_ok= False
    int_button_area_id= int(button_area_id)
    for dep in self.departments:
        for area in dep.areas:
            if area.id==int_button_area_id:
                area_ok= True
    if area_ok:
        area_obj = request.q(SubjectArea).filter(SubjectArea.id == button_area_id).first()
        am = request.q(AreaMember).filter(AreaMember.member_id == self.id).filter(AreaMember.area_id == button_area_id
                                                                              ).first()
        if button_value == 'Y':
            if am is None:
                am = AreaMember(area=area_obj, member=self)
                request.db_session.add(am)
        else:
            if am is not None:
                # Check if user is supporting any propositions in this subject area
                support = request.q(Supporter).filter(Supporter.member == self) \
                    .join(Proposition).join(Ballot).filter(Ballot.area == area_obj) \
                    .filter(Supporter.status == SupporterStatus.ACTIVE) \
                    .filter(Proposition.status == PropositionStatus.SUBMITTED) \
                    .first()
                if not support:
                    request.db_session.delete(am)

    cell = UserCell(self, request)
    return cell.show()
