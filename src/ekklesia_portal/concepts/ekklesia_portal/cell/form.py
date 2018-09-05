from .layout import LayoutCell


class FormCell(LayoutCell):

    def __init__(self, form, request, form_data, collection=None, layout=None, parent=None, template_path=None, **options):
        self.form = form
        self.form_data = form_data or {}
        super().__init__(form, request, collection, layout, parent, template_path, **options)

    def form_html(self):
        return self.__class__.markup_class(self.form.render(self.form_data))
