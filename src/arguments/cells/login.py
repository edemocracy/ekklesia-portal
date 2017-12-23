from arguments.helper.cell import Cell
from arguments.models.login import Login


class LoginCell(Cell):
    model = Login
    model_properties = ['username']
