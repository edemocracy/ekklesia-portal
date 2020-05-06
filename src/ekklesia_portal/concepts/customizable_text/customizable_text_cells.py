from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.ekklesia_portal.cell.form import NewFormCell, EditFormCell
from ekklesia_portal.database.datamodel import CustomizableText
from ekklesia_portal.permission import CreatePermission, EditPermission
from .customizable_texts import CustomizableTexts


@App.cell(CustomizableTexts)
class CustomizableTextsCell(LayoutCell):

    def customizable_texts(self):
        return list(self._model.customizable_texts(self._request.q))

    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


@App.cell(CustomizableText)
class CustomizableTextCell(LayoutCell):

    model_properties = ['lang', 'name', 'text']

    def can_edit(self):
        return self._request.permitted_for_current_user(self._model, EditPermission)

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self.can_edit


@App.cell(CustomizableTexts, 'new')
class NewCustomizableTextCell(NewFormCell):
    pass

@App.cell(CustomizableText, 'edit')
class EditCustomizableTextCell(EditFormCell):
    pass
