from ekklesia_portal.app import App
from ekklesia_portal.identity_policy import NoIdentity

class WritePermission:
    pass

class CreatePermission(WritePermission):
    pass


class EditPermission(WritePermission):
    pass


class SupportPermission(WritePermission):
    pass


class VotePermission(WritePermission):
    pass


class ViewPermission:
    pass


@App.permission_rule(model=object, permission=WritePermission, identity=NoIdentity)
def has_write_permission_not_logged_in(identity, model, permission):
    """Protects all views with write actions from users that aren't logged in."""
    return False
