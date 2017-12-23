from arguments.helper.cell import Cell
from arguments.database.datamodel import Argument


class ArgumentCell(Cell):
    model = Argument
    model_properties = ['title', 'abstract', 'details', 'created_at', 'author']
