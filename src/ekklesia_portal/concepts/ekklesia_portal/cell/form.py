from .layout import LayoutCell


class FormCell(LayoutCell):

    def __init__(self, form, request, form_data=None, model=None, layout=None, parent=None, template_path=None, **options):
        self._form = form
        self._form_data = {k: v for k, v in form_data.items() if v is not None} if form_data is not None else {}
        super().__init__(model, request, None, layout, parent, template_path, **options)

    def _prepare_form_for_render(self):
        pass

    def form_html(self):
        self._prepare_form_for_render()
        html = self._form.render(self._form_data)
        return self.__class__.markup_class(html)


class NewFormCell(FormCell):

    def __init__(self, request, form, form_data=None, layout=None, parent=None, template_path=None, **options):
        super().__init__(form, request, form_data, layout=layout, parent=parent, template_path=template_path, **options)


class EditFormCell(FormCell):

    def _prepare_form_for_render(self):
        self._form_data = self._model.to_dict()

    def __init__(self, model, request, form, layout=None, parent=None, template_path=None, **options):
        super().__init__(form, request, model=model, layout=layout, parent=parent, template_path=template_path, **options)

