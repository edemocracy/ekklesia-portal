from {{ cookiecutter.app_name }}.concepts.{{ cookiecutter.app_name }}.cell.layout import LayoutCell
from {{ cookiecutter.app_name }}.concepts.{{ cookiecutter.app_name }}.cell.form import NewFormCell, EditFormCell
from {{ cookiecutter.app_name }}.database.datamodel import {{ cookiecutter.ConceptName }}
from {{ cookiecutter.app_name }}.permission import CreatePermission, EditPermission
#from .{{ cookiecutter.concept_name }}_helper import items_for_{{cookiecutter.concept_name}}_select_widgets
from .{{ cookiecutter.concept_names }} import {{ cookiecutter.ConceptNames }}


class {{ cookiecutter.ConceptNames }}Cell(LayoutCell):
    model = {{ cookiecutter.ConceptNames }}

    def {{ cookiecutter.concept_names }}(self):
        return list(self._model.{{ cookiecutter.concept_names }}(self._request.q))

    # a method that can be used in the template (works without call parentheses)
    def show_new_button(self):
        return self.options.get('show_new_button') and self._request.permitted_for_current_user(self._model, CreatePermission)


class {{ cookiecutter.ConceptName }}Cell(LayoutCell):
    model = {{ cookiecutter.ConceptName }}
    #model_properties = ['name']

    def show_edit_button(self):
        return self.options.get('show_edit_button') and self._request.permitted_for_current_user(self._model, EditPermission)


class New{{ cookiecutter.ConceptName }}Cell(NewFormCell):

    def _prepare_form_for_render(self):
        pass
        # for select fields
        #items = items_for_{{cookiecutter.concept_name}}_select_widgets(self._model)
        #self._form.prepare_for_render(items)


class Edit{{ cookiecutter.ConceptName }}Cell(EditFormCell):

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        # for select fields
        #items = items_for_{{cookiecutter.concept_name}}_select_widgets(self._model)
        #self._form.prepare_for_render(items)
