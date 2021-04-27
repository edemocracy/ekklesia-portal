from ekklesia_common.permission import ViewPermission
from ekklesia_portal.app import App
from ..admin_area import AdminArea


@App.permission_rule(model=AdminArea, permission=ViewPermission)
def admin_area_view_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=AdminArea, path='/admin')
def admin_area():
    return AdminArea()


@App.html(model=AdminArea, permission=ViewPermission)
def show(self, request):
    from ..cell.admin_area import AdminAreaCell
    return AdminAreaCell(self, request).show()
