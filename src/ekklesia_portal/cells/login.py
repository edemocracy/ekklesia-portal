from ekklesia_portal.helper.cell import Cell
from ekklesia_portal.models.login import Login


class LoginCell(Cell):
    model = Login
    model_properties = ['username']
