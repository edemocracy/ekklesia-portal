import logging

import morepath
from ekklesia_common.identity_policy import NoIdentity
from ekklesia_common.utils import cached_property

from ekklesia_portal.datamodel import User

logg = logging.getLogger(__name__)


class UserIdentity(morepath.Identity):

    def __init__(self, user, refresh_user_object, has_global_admin_permissions=False):
        self._user = user
        self._refresh_user_object = refresh_user_object
        self.has_global_admin_permissions = has_global_admin_permissions
        self.userid = user.id

    @cached_property
    def user(self):
        return self._refresh_user_object(self._user)


class EkklesiaPortalIdentityPolicy(morepath.IdentityPolicy):

    identity_class = UserIdentity

    def remember(self, response, request, identity):
        request.browser_session['user_id'] = identity.user.id

    def identify(self, request):
        user_id = request.browser_session.get('user_id')
        logg.debug('identity policy, user_id is %s', user_id)
        if user_id is None:
            return NoIdentity()

        user = request.db_session.query(User).get(user_id)

        if user is None:
            logg.info('user_id %s in session, but not found in the database!', user_id)
            return NoIdentity()

        def refresh_user_object(user):
            return request.db_session.merge(user)

        return self.identity_class(
            user, refresh_user_object, has_global_admin_permissions=any(g.is_admin_group for g in user.groups)
        )

    def forget(self, response, request):
        if 'user_id' in request.browser_session:
            del request.browser_session['user_id']
