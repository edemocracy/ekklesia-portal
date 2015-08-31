from flask_admin.contrib.sqla import ModelView

from arguments import admin
from arguments.database.datamodel import *


class BaseAdminView(ModelView):

    def __init__(self, model, session=db.session, *args, **kwargs):
        super(BaseAdminView, self).__init__(model, session, *args, **kwargs)


admin.add_view(BaseAdminView(User, category="User"))
admin.add_view(BaseAdminView(UserGroup, category="User"))
admin.add_view(BaseAdminView(Question, category="Content"))
admin.add_view(BaseAdminView(Argument, category="Content"))
admin.add_view(BaseAdminView(Tag, category="Content"))
