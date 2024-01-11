from markupsafe import Markup
from ekklesia_common.debug.tbtools import Traceback

from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.concepts.customizable_text.customizable_text_helper import customizable_text


class ExceptionCell(LayoutCell):

    _model: Exception

    model_properties = ["task_uuid", "xid"]

    @property
    def is_global_admin(self):
        return self._request.current_user and self._request.identity.has_global_admin_permissions

    def show_exception_details(self):
        return self.is_global_admin

    def traceback(self):
        if self.is_global_admin:
            exc = self._model.__cause__
            werkzeug_traceback = Traceback(exc.__class__, exc, exc.__traceback__)
            return Markup(werkzeug_traceback.render_full())

    def help_text(self):
        return customizable_text(self._request, 'unhandled_exception_help_text')
