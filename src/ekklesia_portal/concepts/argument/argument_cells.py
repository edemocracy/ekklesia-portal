from ekklesia_common.cell import Cell

from ekklesia_portal.app import App
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell
from ekklesia_portal.datamodel import Argument


@App.cell()
class ArgumentCell(LayoutCell):

    _model: Argument
    model_properties = ['id', 'title', 'abstract', 'details', 'created_at', 'author']

    footer = Cell.fragment('argument_footer')

    def details_link(self):
        if 'details_link' in self.options:
            return self.options['details_link']

        return self.self_link
