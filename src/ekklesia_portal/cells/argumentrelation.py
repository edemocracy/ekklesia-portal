from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.database.datamodel import ArgumentRelation


class ArgumentRelationCell(Cell):
    model = ArgumentRelation
    model_properties = ['id', 'proposition', 'argument', 'score']

    @property
    def show_voting(self):
        return self.current_user is not None

    @property
    def show_ca_button(self):
        return # self.current_user is not None

    @property
    def vote(self):
        return self._model.user_vote(self.current_user)

    @property
    def proposition_url(self):
        return self.link(self._model.proposition)

    @property
    def argument_url(self):
        return self.link(self._model.argument)

    @property
    def proposition_title(self):
        return self.proposition.title

    @property
    def argument_title(self):
        return self.argument.title

    @property
    def upvote_button_disabled_class(self):
        return 'disabled' if self.vote is not None and self.vote.weight == 1 else ''

    @property
    def downvote_button_disabled_class(self):
        return 'disabled' if self.vote is not None and self.vote.weight == -1 else ''

    @property
    def revoke_vote_button_disabled_class(self):
        return 'disabled' if self.vote is None or self.vote.weight == 0 else ''

    @property
    def vote_action_url(self):
        return self.link(self._model, 'vote')
