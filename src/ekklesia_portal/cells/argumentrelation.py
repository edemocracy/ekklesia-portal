from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.database.datamodel import ArgumentRelation


class ArgumentRelationCell(Cell):
    model = ArgumentRelation
    model_properties = ['id', 'proposition', 'argument', 'score']

    def show_voting(self):
        return self.current_user is not None

    def show_ca_button(self):
        return # self.current_user is not None

    def vote(self):
        return self._model.user_vote(self.current_user)

    def proposition_url(self):
        return self.link(self._model.proposition)

    def argument_url(self):
        return self.link(self._model.argument)

    def proposition_title(self):
        return self.proposition.title

    def argument_title(self):
        return self.argument.title

    def upvote_button_disabled_class(self):
        return 'disabled' if self.vote is not None and self.vote.weight == 1 else ''

    def downvote_button_disabled_class(self):
        return 'disabled' if self.vote is not None and self.vote.weight == -1 else ''

    def revoke_vote_button_disabled_class(self):
        return 'disabled' if self.vote is None or self.vote.weight == 0 else ''

    def vote_action_url(self):
        return self.link(self._model, 'vote')
