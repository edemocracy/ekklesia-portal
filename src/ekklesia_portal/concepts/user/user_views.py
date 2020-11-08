from ekklesia_portal.app import App
from ekklesia_portal.datamodel import User, AreaMember, SubjectArea
from ekklesia_portal.permission import ViewPermission

from .user_cells import UserCell


@App.permission_rule(model=User, permission=ViewPermission)
def user_view_permission(identity, model, permission):
    # XXX identity.user is detached, must compare ids instead of objects
    return identity.user.id == model.id


@App.path(model=User, path='/u/{name}')
def user(request, name):
    user = request.q(User).filter_by(name=name).scalar()
    return user


@App.html(model=User, permission=ViewPermission)
def show(self, request):
    cell = UserCell(self, request)
    return cell.show()


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
                request.db_session.delete(am)

    cell = UserCell(self, request)
    return cell.show()
