
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import User
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
