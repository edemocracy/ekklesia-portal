from morepath import reify
from more.babel_i18n import BabelRequest

from ekklesia_portal import database


class EkklesiaPortalRequest(BabelRequest):

    @reify
    def db_session(self):
        return database.Session()

    def q(self, *args, **kwargs):
        return self.db_session.query(*args, **kwargs)

    def render_template(self, template, **context):
        template = self.app.jinja_env.get_template(template)
        return template.render(**context)
