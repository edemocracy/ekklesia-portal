import logging
import morepath
from ekklesia_portal.database.datamodel import User


logg = logging.getLogger(__name__)


class EkklesiaPortalIdentityPolicy(morepath.IdentityPolicy):

    identity_class = morepath.Identity
 
    def remember(self, response, request, identity):
        request.browser_session['user_id'] = identity.user.id

    def identify(self, request):
        user_id = request.browser_session.get('user_id')
        if user_id is None:
            return morepath.NO_IDENTITY

        user = request.db_session.query(User).get(user_id)

        if user is None:
            logg.info('user_id %s in session, but not found in the database!', user_id)
            return morepath.NO_IDENTITY

        return self.identity_class(userid=user_id, user=user)

    def forget(self, response, request):
        del request.browser_session['user_id']
