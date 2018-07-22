from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.cells.layout import LayoutCell
from ekklesia_portal.database.datamodel import ArgumentRelation
from ekklesia_portal.forms import ArgumentForPropositionForm
from ekklesia_portal.permission import VotePermission


class ArgumentRelationCell(LayoutCell):
    model = ArgumentRelation
    model_properties = ['id', 'proposition', 'argument', 'score']

    def show_voting(self):
        return self._request.permitted_for_current_user(self._model, VotePermission)

    def show_ca_button(self):
        return  # self.current_user is not None

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


class NewArgumentForPropositionCell(LayoutCell):
    model = ArgumentForPropositionForm

    def __init__(self, form, request, form_data, proposition, collection=None, layout=None, parent=None, template_path=None, **options):
        self.form = form
        self.form_data = form_data or {}
        self.proposition = proposition
        super().__init__(form, request, collection, layout, parent, template_path, **options)

    def form_html(self):
        return Cell.markup_class(self.form.render(self.form_data))
