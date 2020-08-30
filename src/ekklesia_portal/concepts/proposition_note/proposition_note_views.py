from ekklesia_common.lid import LID
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


@App.path(model=PropositionNote, path='proposition_notes/{proposition_id}/{user_id}')
def proposition_note(request, proposition_id=LID(), user_id=0):
    note = request.q(PropositionNote).get({"proposition_id": proposition_id, "user_id": user_id})
    if note is None:
        return PropositionNote(user_id, proposition_id)

    return note


@App.html(model=PropositionNote, name='edit', permission=EditPermission)
def edit(self, request):
    form = PropositionNoteForm(request, request.link(self))
    return EditPropositionNoteCell(self, request, form).show()


@App.html_form_post(
    model=PropositionNote, form=PropositionNoteForm, cell=EditPropositionNoteCell, permission=EditPermission
)
def update(self, request, appstruct):
    request.db_session.add(self)
    self.update(**appstruct)
    prop = request.q(Proposition).get({"id": appstruct["proposition_id"]})
    return redirect(request.link(prop))
