#from flask_admin.contrib.sqla import ModelView

#from arguments import admin
#from arguments.database.datamodel import *


#class BaseAdminView(ModelView):

#    def __init__(self, model, session=db.session, *args, **kwargs):
#        super(BaseAdminView, self).__init__(model, session, *args, **kwargs)


#class QuestionView(ModelView):
#    column_exclude_list = ("details", "search_vector")

#    def __init__(self, session=db.session, *args, **kwargs):
#        super(QuestionView, self).__init__(Question, session, category="Content", *args, **kwargs)


#admin.add_view(BaseAdminView(User, category="User"))
#admin.add_view(BaseAdminView(UserGroup, category="User"))
#admin.add_view(QuestionView())
#admin.add_view(BaseAdminView(Argument, category="Content"))
#admin.add_view(BaseAdminView(Tag, category="Content"))
#admin.add_view(BaseAdminView(QuestionVote, category="Vote"))
#admin.add_view(BaseAdminView(VotingModule, category="Configuration"))
#admin.add_view(BaseAdminView(ArgumentVote, category="Vote"))
