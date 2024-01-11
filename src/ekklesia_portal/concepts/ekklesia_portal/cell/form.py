from .layout import LayoutCell
from ekklesia_common.cell import EditCellMixin, NewCellMixin


class FormCell(LayoutCell):

    def __init__(
        self, request, form, form_data=None, model=None, layout=None, parent=None, template_path=None, **options
    ):
        self._form = form
        if form_data is not None:
            self.set_form_data(form_data)
        else:
            self._form_data = None
        super().__init__(model, request, None, layout, parent, template_path, **options)

    def _prepare_form_for_render(self):
        pass

    def set_form_data(self, form_data):
        self._form_data = {k: v for k, v in form_data.items() if v is not None}

    def form_html(self):
        self._prepare_form_for_render()
        if self._form_data is None:
            html = self._form.render()
        else:
            html = self._form.render(self._form_data)

        return self.__class__.markup_class(html)


class NewFormCell(FormCell, NewCellMixin):

    def __init__(
        self, request, form, form_data=None, model=None, layout=None, parent=None, template_path=None, **options
    ):
        super().__init__(
            request, form, form_data, model=model, layout=layout, parent=parent, template_path=template_path, **options
        )

    def _prepare_form_for_render(self):
        self._form.prepare_for_render()


class EditFormCell(FormCell, EditCellMixin):

    def __init__(self, model, request, form, form_data=None, layout=None, parent=None, template_path=None, **options):
        super().__init__(
            request, form, form_data, model=model, layout=layout, parent=parent, template_path=template_path, **options
        )

    def _prepare_form_for_render(self):
        form_data = self._model.to_dict()
        self.set_form_data(form_data)
        self._form.prepare_for_render()
