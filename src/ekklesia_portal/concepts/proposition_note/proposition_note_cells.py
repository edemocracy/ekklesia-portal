from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import PropositionNote
from ekklesia_portal.permission import CreatePermission, EditPermission

from .proposition_note_helper import items_for_proposition_note_select_widgets
from .proposition_notes import PropositionNotes


class PropositionNotesCell(LayoutCell):
    model = PropositionNotes

    def proposition_notes(self):
        return list(self._model.proposition_notes(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button'
                                ) and self._request.permitted_for_current_user(self._model, CreatePermission)


class PropositionNoteCell(LayoutCell):
    model = PropositionNote

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)


class NewPropositionNoteCell(NewFormCell):
    pass


class EditPropositionNoteCell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        items = items_for_proposition_note_select_widgets(self._model)
        self._form.prepare_for_render(items)
