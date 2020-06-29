from morepath import redirect
from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Proposition, PropositionNote
from ekklesia_portal.permission import EditPermission
from .proposition_note_cells import EditPropositionNoteCell
from .proposition_note_contracts import PropositionNoteForm


@App.permission_rule(model=PropositionNote, permission=EditPermission)
def proposition_note_edit_permission(identity, model, permission):
    tmp = identity.user.id == int(model.user_id)
    return tmp


@App.path(model=PropositionNote, path='n/{proposition_id}/{user_id}')
def proposition_note(request, proposition_id, user_id):
    note = request.q(PropositionNote).get({"proposition_id": proposition_id, "user_id": user_id})
    if note is None:
        return PropositionNote(user_id, proposition_id)
    else:
        return note


@App.html(model=PropositionNote, name='edit', permission=EditPermission)
def edit(self, request):
    form = PropositionNoteForm(request, request.link(self))
    tmp = EditPropositionNoteCell(self, request, form).show()
    return tmp


@App.html_form_post(model=PropositionNote, form=PropositionNoteForm, cell=EditPropositionNoteCell, permission=EditPermission)
def update(self, request, appstruct):
    request.db_session.add(self)
    self.update(**appstruct)
    prop = request.q(Proposition).get({"id": appstruct["proposition_id"]})
    return redirect(request.link(prop))
