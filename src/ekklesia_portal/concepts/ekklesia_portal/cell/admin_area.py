from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ..admin_area import AdminArea
from ..admin_box import AdminBox


@App.cell(AdminArea)
class AdminAreaCell(LayoutCell):

    def admin_box(self):
        return AdminBox()

    def is_global_admin(self):
        return self._request.current_user and self._request.identity.has_global_admin_permissions

    def managed_departments(self):
        return self.current_user.managed_departments

    def queued_messages(self):
        return [
            dict(author="testuser", subject="Bitte Antrag XY löschen", body="War ne blöde Idee, sorry"),
            dict(author="testadmin", subject="Schau dir mal user testuser an", body="Macht komische Dinge"),
            dict(author="testuser", subject="Bitte Antrag XY löschen", body="War ne blöde Idee, sorry"),
            dict(),
            dict(),
            dict(),
            dict(),
            dict(),
        ]

    def queued_propositions(self):
        return [
            dict(author="testuser", title="Antrag XY", content="Der Vorstand wird verpflichtet..."),
            dict(author="testuser", title="Antrag 1", content="..."),
            dict(author="testuser", title="Antrag 2", content="..."),
            dict(),
            dict(),
            dict(),
            dict(),
            dict(),
            dict(),
        ]
