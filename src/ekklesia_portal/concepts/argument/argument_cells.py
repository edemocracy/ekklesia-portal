from ekklesia_common.cell import Cell
from ekklesia_portal.database.datamodel import Argument
from ekklesia_portal.concepts.ekklesia_portal.cell.layout import LayoutCell


class ArgumentCell(LayoutCell):
    model = Argument
    model_properties = ['id', 'title', 'abstract', 'details', 'created_at', 'author']

    footer = Cell.fragment('argument_footer')

    def details_link(self):
        if 'details_link' in self.options:
            return self.options['details_link']

        return self.self_link
