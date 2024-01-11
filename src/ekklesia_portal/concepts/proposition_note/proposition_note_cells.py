from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.form import EditFormCell, NewFormCell
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import PropositionNote
from ekklesia_portal.permission import CreatePermission, EditPermission

from .proposition_note_helper import items_for_proposition_note_select_widgets
from .proposition_notes import PropositionNotes


@App.cell()
class PropositionNotesCell(LayoutCell):

    _model: PropositionNotes

    def proposition_notes(self):
        return list(self._model.proposition_notes(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button'
                                ) and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell()
class PropositionNoteCell(LayoutCell):

    _model: PropositionNote

    def show_edit_button(self):
        return self.options.get('show_edit_button'
                                ) and self._request.permitted_for_current_user(self._model, EditPermission)


@App.cell()
class NewPropositionNoteCell(NewFormCell):

    _model: PropositionNotes


@App.cell()
class EditPropositionNoteCell(EditFormCell):

    _model: PropositionNote

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        items = items_for_proposition_note_select_widgets(self._model)
        self._form.prepare_for_render(items)
