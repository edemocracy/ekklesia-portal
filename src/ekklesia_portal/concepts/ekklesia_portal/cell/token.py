from ekklesia_portal.concepts.ekklesia_portal.cell.form import FormCell
from ekklesia_portal.datamodel import Page


class TokenCell(FormCell):

    def content_token_login(self):
        return (self._request.q(Page.text).filter_by(name='content_token_login', lang=self.language).scalar())
