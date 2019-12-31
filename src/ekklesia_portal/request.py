import morepath
from ekklesia_common.utils import cached_property

from ekklesia_portal import database


class EkklesiaPortalRequest(morepath.Request):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def db_session(self):
        return database.Session()

    @cached_property
    def current_user(self):
        user = self.identity.user
        if user is None:
            return
        user = self.db_session.merge(user)
        return user

    def permitted_for_current_user(self, obj, permission):
        return self.app._permits(self.identity, obj, permission)

    def q(self, *args, **kwargs):
        return self.db_session.query(*args, **kwargs)

    def render_template(self, template, **context):
        template = self.app.jinja_env.get_template(template)
        return template.render(**context)


Request = EkklesiaPortalRequest
