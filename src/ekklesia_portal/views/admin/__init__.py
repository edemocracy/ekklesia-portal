#from flask_admin.contrib.sqla import ModelView

#from ekklesia_portal import admin
#from ekklesia_portal.database.datamodel import *


#class BaseAdminView(ModelView):

#    def __init__(self, model, session=db.session, *args, **kwargs):
#        super(BaseAdminView, self).__init__(model, session, *args, **kwargs)


#class PropositionView(ModelView):
#    column_exclude_list = ("details", "search_vector")

#    def __init__(self, session=db.session, *args, **kwargs):
#        super(PropositionView, self).__init__(Proposition, session, category="Content", *args, **kwargs)


#admin.add_view(BaseAdminView(User, category="User"))
#admin.add_view(BaseAdminView(UserGroup, category="User"))
#admin.add_view(PropositionView())
#admin.add_view(BaseAdminView(Argument, category="Content"))
#admin.add_view(BaseAdminView(Tag, category="Content"))
#admin.add_view(BaseAdminView(PropositionVote, category="Vote"))
#admin.add_view(BaseAdminView(VotingModule, category="Configuration"))
#admin.add_view(BaseAdminView(ArgumentVote, category="Vote"))
