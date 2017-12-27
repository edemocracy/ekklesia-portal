from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.database.datamodel import Argument


class ArgumentCell(Cell):
    model = Argument
    model_properties = ['title', 'abstract', 'details', 'created_at', 'author']
