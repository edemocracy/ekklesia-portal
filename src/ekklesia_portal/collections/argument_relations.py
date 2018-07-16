from ekklesia_portal.forms import ArgumentForPropositionForm


class ArgumentRelations:
    def __init__(self, proposition_id=None, relation_type=None):
        self.proposition_id = proposition_id
        self.relation_type = relation_type

    def form(self, action):
        return ArgumentForPropositionForm(action)
