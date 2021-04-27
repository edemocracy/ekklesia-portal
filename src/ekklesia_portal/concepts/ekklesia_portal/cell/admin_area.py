from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ..admin_area import AdminArea
from ..admin_box import AdminBox


@App.cell(AdminArea)
class AdminAreaCell(LayoutCell):

    def admin_box(self):
        return AdminBox()

